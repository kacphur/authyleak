````md
<div align="center">

```text
 █████╗ ██╗   ██╗████████╗██╗  ██╗██╗   ██╗██╗     ███████╗ █████╗ ██╗  ██╗
██╔══██╗██║   ██║╚══██╔══╝██║  ██║╚██╗ ██╔╝██║     ██╔════╝██╔══██╗██║ ██╔╝
███████║██║   ██║   ██║   ███████║ ╚████╔╝ ██║     █████╗  ███████║█████╔╝
██╔══██║██║   ██║   ██║   ██╔══██║  ╚██╔╝  ██║     ██╔══╝  ██╔══██║██╔═██╗
██║  ██║╚██████╔╝   ██║   ██║  ██║   ██║   ███████╗███████╗██║  ██║██║  ██╗
╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝
```

*find osu! auth tokens & memory offsets.*

</div>

---

```txt
> status

platform  :: windows
python    :: 3.10+
target    :: osu!.exe
version   :: 3.1
```

## install

```powershell
git clone https://github.com/kacphur/authyleak

cd authyleak

installer.bat
```

or

```powershell
pip install pymem rich psutil pywin32

python authyleak.py
```

---

## functions

```txt
[01] auth token scanner
[02] audio offset finder
[03] left mouse address
[04] right mouse address
[05] mouse position pointer
```

---

<details>
<summary><b>preview</b></summary>

```txt
v3.1.0 │ 20:54:18 │ attached to osu!.exe

1. find auth token
2. find audio offset
3. find left mouse button
4. find right mouse button
5. find mouse pointer

>
```

</details>

---

```txt
> notes

• run as administrator
• keep osu! open
• installer installs missing packages automatically
• works in windows terminal
```

<div align="center">

```txt
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

built for osu-ac research

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

</div>
````
