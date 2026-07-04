#!/usr/bin/env python3
# authyleak v3.1 – Complete Osu! Auth & Offset Finder (Windows Terminal)
import sys, os, subprocess, ctypes, time, datetime
import pymem, pymem.process, psutil
import win32gui, win32process, win32con, win32api
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

# ─── Colour palette ─────────────────────────────────────
PINK  = "#FF66AA"
WHITE = "#FFFFFF"
DIM   = "#AAAAAA"

console = Console(highlight=False)

def log(msg):
    ts = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
    console.print(f"[{WHITE}]v3.1.0[/{WHITE}]  [{DIM}]┃[/{DIM}]  [{WHITE}]{ts}[/{WHITE}]  [{DIM}]┃[/{DIM}]  [{PINK}]{msg}[/{PINK}]")

ASCII_ART = r"""
[bold #FF66AA]
    █████╗ ██╗   ██╗████████╗██╗  ██╗██╗   ██╗██╗     ███████╗ █████╗ ██╗  ██╗
   ██╔══██╗██║   ██║╚══██╔══╝██║  ██║╚██╗ ██╔╝██║     ██╔════╝██╔══██╗██║ ██╔╝
   ███████║██║   ██║   ██║   ███████║ ╚████╔╝ ██║     █████╗  ███████║█████╔╝ 
   ██╔══██║██║   ██║   ██║   ██╔══██║  ╚██╔╝  ██║     ██╔══╝  ██╔══██║██╔═██╗ 
   ██║  ██║╚██████╔╝   ██║   ██║  ██║   ██║   ███████╗███████╗██║  ██║██║  ██╗
   ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝
[/bold #FF66AA]
[#FFFFFF]              Osu! Auth Leaker & Memory Offset Finder (osu‑ac compatible)[/#FFFFFF]
"""

# ─── Admin & Terminal helpers ───────────────────────────
def is_admin():
    try: return ctypes.windll.shell32.IsUserAnAdmin()
    except: return False

def run_as_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{__file__}"', None, 1)
    sys.exit(0)

def in_windows_terminal():
    return os.environ.get("WT_SESSION") is not None

def launch_wt():
    # Try to find wt.exe
    wt = None
    possible = [
        os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WindowsApps\wt.exe"),
        r"C:\Program Files\WindowsApps\Microsoft.WindowsTerminal_8wekyb3d8bbwe\wt.exe"
    ]
    for p in possible:
        if os.path.isfile(p):
            wt = p
            break
    if not wt:
        return  # fallback: stay in current console
    cmd = f'"{wt}" -d "{os.getcwd()}" --title "AUTHYLEAK" cmd /c "python -u authyleak.py"'
    subprocess.Popen(cmd, shell=True)
    sys.exit(0)

def ensure_environment():
    if not is_admin():
        log("Requesting admin privileges…")
        run_as_admin()
    # We are admin now. If not in WT, relaunch in WT.
    if not in_windows_terminal():
        log("Launching Windows Terminal for best visuals…")
        launch_wt()

def install_dependencies():
    deps = {"pymem": "pymem", "rich": "rich", "psutil": "psutil", "pywin32": "win32api"}
    missing = []
    for pip_name, import_name in deps.items():
        try: __import__(import_name)
        except ImportError: missing.append(pip_name)
    if missing:
        print(f"Installing missing: {', '.join(missing)}")
        for m in missing:
            subprocess.check_call([sys.executable, "-m", "pip", "install", m],
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.execv(sys.executable, [sys.executable] + sys.argv)

# ─── Osu! process info ──────────────────────────────────
def get_osu_process_info():
    for proc in psutil.process_iter(['pid', 'name', 'exe', 'memory_info', 'num_threads']):
        if proc.info['name'] and proc.info['name'].lower() == 'osu!.exe':
            pid = proc.info['pid']
            info = {
                'pid': pid,
                'exe': proc.info['exe'],
                'rss': proc.info['memory_info'].rss,
                'threads': proc.info['num_threads']
            }
            # Find main window
            try:
                def cb(hwnd, lParam):
                    if win32process.GetWindowThreadProcessId(hwnd)[1] == pid:
                        text = win32gui.GetWindowText(hwnd)
                        rect = win32gui.GetWindowRect(hwnd)
                        if text and (rect[2]-rect[0]) > 100:
                            info['title'] = text
                            info['width'] = rect[2]-rect[0]
                            info['height'] = rect[3]-rect[1]
                            return False
                    return True
                win32gui.EnumWindows(cb, None)
            except: pass
            return info
    return None

def show_osu_info(pm):
    info = get_osu_process_info()
    if not info:
        log("osu! process info unavailable.")
        return
    lines = []
    lines.append(f"[{WHITE}]PID:[/{WHITE}] [{PINK}]{info['pid']}[/{PINK}]")
    lines.append(f"[{WHITE}]Executable:[/{WHITE}] [{DIM}]{info.get('exe','?')}[/{DIM}]")
    mb = info['rss'] / 1024 / 1024
    lines.append(f"[{WHITE}]Memory:[/{WHITE}] [{PINK}]{mb:.1f} MB[/{PINK}]")
    lines.append(f"[{WHITE}]Threads:[/{WHITE}] [{PINK}]{info.get('threads','?')}[/{PINK}]")
    if 'title' in info:
        lines.append(f"[{WHITE}]Window:[/{WHITE}] [{PINK}]{info['title']}[/{PINK}]")
        lines.append(f"[{WHITE}]Resolution:[/{WHITE}] [{PINK}]{info['width']}x{info['height']}[/{PINK}]")
    panel = Panel("\n".join(lines), title="[bold #FF66AA]osu! Process Info[/bold #FF66AA]", border_style="#FF66AA")
    console.print(panel)

# ─── Memory scanner class ───────────────────────────────
class MemoryScanner:
    def __init__(self, pm, size=4):
        self.pm = pm
        self.size = size
        self.candidates = []
        self.last_values = {}

    def scan_all(self):
        log("Scanning committed writable memory regions...")
        self.candidates = []
        for region in self.pm.list_mapped_regions():
            try:
                if region.State & 0x1000 and region.Protect & 0x04:  # MEM_COMMIT + PAGE_READWRITE
                    if region.RegionSize > 0x1000000:
                        continue
                    data = self.pm.read_bytes(region.BaseAddress, region.RegionSize)
                    for off in range(0, len(data)-self.size+1, self.size):
                        self.candidates.append(region.BaseAddress+off)
            except: continue
        log(f"Initial candidates: {len(self.candidates)}")
        self.snapshot()

    def snapshot(self):
        self.last_values.clear()
        for addr in self.candidates:
            try:
                val = self.pm.read_int(addr) if self.size==4 else self.pm.read_bytes(addr,self.size)[0]
                self.last_values[addr] = val
            except: pass

    def next_scan(self, cmp):
        new = []
        for addr in self.candidates:
            try:
                cur = self.pm.read_int(addr) if self.size==4 else self.pm.read_bytes(addr,self.size)[0]
                prev = self.last_values.get(addr,cur)
                if cmp=='inc' and cur>prev: new.append(addr)
                elif cmp=='dec' and cur<prev: new.append(addr)
                elif cmp=='unchanged' and cur==prev: new.append(addr)
                elif cmp=='changed' and cur!=prev: new.append(addr)
            except: continue
        self.candidates = new
        log(f"Candidates left: {len(self.candidates)}")
        self.snapshot()

# ─── Offset finders ─────────────────────────────────────
def find_audio_offset(pm):
    log("=== AUDIO OFFSET SCANNER ===")
    log("Start a map, pause at the very beginning. Press Enter.")
    input()
    scanner = MemoryScanner(pm, 4)
    scanner.scan_all()
    log("Now play a few seconds, pause again, and use these commands:")
    console.print(f"[{PINK}]I[/{PINK}] = value increased   [{PINK}]D[/{PINK}] = value decreased   [{PINK}]U[/{PINK}] = unchanged   [{PINK}]Q[/{PINK}] = quit")
    while True:
        cmd = input("> ").strip().lower()
        if cmd == 'q': break
        elif cmd == 'i': scanner.next_scan('inc')
        elif cmd == 'd': scanner.next_scan('dec')
        elif cmd == 'u': scanner.next_scan('unchanged')
        if len(scanner.candidates) <= 5:
            log("Possible addresses:")
            for a in scanner.candidates:
                try: val = pm.read_int(a); log(f"  {hex(a)} = {val}")
                except: pass
            break
    if scanner.candidates:
        best = scanner.candidates[0]
        log(f"Audio offset address: {hex(best)} (line 1 of address.txt)")
        return best
    log("No audio offset found.")
    return None

def find_button(pm, name="LMB"):
    log(f"=== {name} BUTTON SCANNER ===")
    log("Play a replay where you click that button ONCE, hold briefly, release. Press Enter before any click.")
    input()
    scanner = MemoryScanner(pm, 1)
    scanner.scan_all()
    console.print(f"[{PINK}]I[/{PINK}] = button pressed (1)   [{PINK}]D[/{PINK}] = button released (0)   [{PINK}]Q[/{PINK}] = quit")
    while True:
        cmd = input("> ").strip().lower()
        if cmd == 'q': break
        elif cmd == 'i': scanner.next_scan('inc')
        elif cmd == 'd': scanner.next_scan('dec')
        if len(scanner.candidates) <= 5:
            log("Candidates (value shown):")
            for a in scanner.candidates:
                try: val = pm.read_bytes(a,1)[0]; log(f"  {hex(a)} = {val}")
                except: pass
            break
    if scanner.candidates:
        best = scanner.candidates[0]
        log(f"{name} address: {hex(best)} (line {'4' if name=='LMB' else '3'} of address.txt)")
        return best
    log(f"No {name} address found.")
    return None

def find_mouse_pointer(pm):
    log("=== MOUSE POSITION POINTER (Y‑based) ===")
    hwnd = win32gui.FindWindow(None, "osu!")
    if not hwnd:
        log("osu! window not found. Run in windowed mode.")
        return None
    rect = win32gui.GetWindowRect(hwnd)
    win_height = rect[3] - rect[1]
    log(f"Window height: {win_height} pixels.")
    log("Move cursor to the TOP of the osu! window, press Enter.")
    input()
    scanner = MemoryScanner(pm, 4)
    scanner.scan_all()
    console.print(f"[{PINK}]I[/{PINK}] = cursor moving DOWN (Y inc)   [{PINK}]D[/{PINK}] = cursor moving UP (Y dec)   [{PINK}]U[/{PINK}] = not moving   [{PINK}]Q[/{PINK}] = quit")
    while True:
        cmd = input("> ").strip().lower()
        if cmd == 'q': break
        elif cmd == 'i': scanner.next_scan('inc')
        elif cmd == 'd': scanner.next_scan('dec')
        elif cmd == 'u': scanner.next_scan('unchanged')
        if len(scanner.candidates) <= 10:
            log("Potential Y positions:")
            for a in scanner.candidates:
                try:
                    val = pm.read_int(a)
                    if 0 <= val <= win_height:
                        log(f"  {hex(a)} = {val} (in range)")
                except: pass
            break
    # Pick first candidate within screen height
    for a in scanner.candidates:
        try:
            val = pm.read_int(a)
            if 0 <= val <= win_height:
                log(f"Mouse pointer base: {hex(a)} (line 2 of address.txt)")
                return a
        except: continue
    log("Could not isolate pointer. Try again.")
    return None

def find_auth_token(pm):
    log("Scanning for JWT auth tokens...")
    pattern = b'\x65\x79\x4A'   # "eyJ"
    try:
        mod = pymem.process.module_from_name(pm.process_handle, "osu!.exe")
        addrs = pymem.pattern.scan_pattern_module(pm.process_handle, mod, pattern, return_multiple=True)
    except:
        addrs = pymem.pattern.scan_pattern_page(pm.process_handle, pattern, return_multiple=True)
    tokens = []
    for addr in addrs:
        try:
            data = pm.read_bytes(addr, 4096)
            token_bytes = data.split(b'\x00')[0]
            token_str = token_bytes.decode('utf-8', errors='ignore')
            if token_str.count('.') == 2 and len(token_str) > 50:
                tokens.append((addr, token_str))
        except: continue
    if tokens:
        table = Table(title="[bold #FF66AA]Auth Tokens[/bold #FF66AA]", border_style="#FF66AA")
        table.add_column("Address", style="#FF66AA")
        table.add_column("Token", style="#FFFFFF")
        table.add_column("Length", style="#FF66AA")
        for a, t in tokens:
            table.add_row(hex(a), t[:80]+"..." if len(t)>80 else t, str(len(t)))
        console.print(table)
        log(f"Found {len(tokens)} token(s).")
    else:
        log("No tokens found.")
    return tokens

# ─── Main menu ──────────────────────────────────────────
def main():
    ensure_environment()
    install_dependencies()
    console.clear()
    console.print(ASCII_ART)
    log("Welcome to authyleak v3.1 (Complete Edition)")

    # Attach to osu! (wait if needed)
    pm = None
    while not pm:
        info = get_osu_process_info()
        if info:
            try:
                pm = pymem.Pymem("osu!.exe")
                show_osu_info(pm)
                break
            except Exception as e:
                log(f"Failed to attach: {e}")
                input("Press Enter to exit...")
                return
        else:
            log("osu!.exe not running!")
            choice = console.input(f"[{PINK}]Wait for osu! to start? (y/n): [/{PINK}]")
            if choice.strip().lower() != 'y':
                log("Exiting.")
                input("Press Enter to close...")
                return
            time.sleep(3)

    # Main loop
    while True:
        console.print(f"\n[{PINK}]Choose a mode:[/{PINK}]")
        console.print(f"[{WHITE}]1[/{WHITE}] - Find Auth Token")
        console.print(f"[{WHITE}]2[/{WHITE}] - Find Audio Offset (osu-ac line 1)")
        console.print(f"[{WHITE}]3[/{WHITE}] - Find Left Mouse Button (osu-ac line 4)")
        console.print(f"[{WHITE}]4[/{WHITE}] - Find Right Mouse Button (osu-ac line 3)")
        console.print(f"[{WHITE}]5[/{WHITE}] - Find Mouse Position Pointer (osu-ac line 2)")
        console.print(f"[{WHITE}]6[/{WHITE}] - Exit")
        choice = console.input(f"[{PINK}]Enter choice: [/{PINK}]").strip()
        if choice == '1':
            find_auth_token(pm)
        elif choice == '2':
            find_audio_offset(pm)
        elif choice == '3':
            find_button(pm, "LMB")
        elif choice == '4':
            find_button(pm, "RMB")
        elif choice == '5':
            find_mouse_pointer(pm)
        elif choice == '6':
            log("Shutting down. Stay rebel. 🏴‍☠️")
            break
        else:
            log("Invalid option.")
    input("Press Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log(f"Unexpected error: {e}")
        input("Press Enter to exit...")