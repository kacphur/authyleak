```md
<div align="center">

# authyleak

```

█████╗ ██╗   ██╗████████╗██╗  ██╗██╗   ██╗██╗     ███████╗ █████╗ ██╗  ██╗
██╔══██╗██║   ██║╚══██╔══╝██║  ██║╚██╗ ██╔╝██║     ██╔════╝██╔══██╗██║ ██╔╝
███████║██║   ██║   ██║   ███████║ ╚████╔╝ ██║     █████╗  ███████║█████╔╝
██╔══██║██║   ██║   ██║   ██╔══██║  ╚██╔╝  ██║     ██╔══╝  ██╔══██║██╔═██╗
██║  ██║╚██████╔╝   ██║   ██║  ██║   ██║   ███████╗███████╗██║  ██║██║  ██╗
╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝

````

finds osu! auth tokens and memory offsets.

</div>

---

## what it does

authyleak attaches to `osu!.exe` and helps you find:

- jwt auth tokens
- audio offset
- mouse position pointer
- left mouse button address
- right mouse button address

made for finding the values needed by osu-ac.

---

## features

- automatic dependency installer
- auto admin request
- windows terminal support
- interactive memory scanner
- simple menu
- coloured terminal ui

---

## requirements

- windows
- python 3.10+
- osu! running

---

## install

```bash
git clone https://github.com/kacphur/authyleak

cd authyleak

installer.bat
````

or

```bash
pip install pymem rich psutil pywin32
python authyleak.py
```

---

## menu

```text
1. find auth token

2. find audio offset

3. find left mouse button

4. find right mouse button

5. find mouse pointer

6. exit
```

---

## notes

run as administrator.

leave osu! open before scanning.

---

## license

mit

```
```
