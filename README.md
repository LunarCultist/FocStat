# Focal Length Histogram Generator

**Version:** 1.0
**Author:** Shotokanda
**License:** [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) – Non-commercial use only, attribution required

---

## 📸 What is this?

This is a graphical tool that helps photographers analyze which focal lengths they use most. It scans JPG files in selected folders and creates a histogram of focal lengths from the EXIF data.

Supported features:
- Select multiple image folders
- View a histogram of used focal lengths
- Multilingual interface: English, Deutsch, 日本語
- Platform independent (Windows, Linux, macOS)

---

## 🖥️ How to Run

### ✅ Windows Users
1. Download the latest release from the [Releases](https://github.com/yourname/focstat/releases) page
2. Unzip the file
3. Double-click `Focstat.exe` to start

> No installation required if using the EXE. If you want to run from source, see below.

### ✅ Linux / macOS Users
1. Make sure `python3` is installed
2. Install required dependencies:

```bash
sudo apt install python3 python3-pip exiftool  # Linux only
pip3 install -r requirements.txt
```

3. Start the application:

```bash
python3 focstat.py
```

---

## 📦 Dependencies

Listed in `requirements.txt`:
- PyQt5
- matplotlib
- exifread

Install with:
```bash
pip install -r requirements.txt
```

---

## 🔧 Developer Info

To build a Windows `.exe` yourself:
```bash
pip install pyinstaller
pyinstaller focstat.py --onefile --windowed --icon app_icon.ico --name Focstat
```
Output will be in the `dist/` folder.

---

## 📄 License

This software is licensed under the Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0) license.
You may **not** sell this software.
You **must** give attribution to the author: **Shotokanda**.
