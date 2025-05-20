# Ghost Mode 👻

![Python Version](https://img.shields.io/badge/python-3.8+-blue)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20linux-lightgrey)

System-wide privacy toggle with hardware control, process termination, and location spoofing.

## Features
- 🎥 Webcam disable
- 🎤 Microphone mute
- 📍 GPS spoofing (Windows)
- 📶 MAC randomization (Linux)
- ⚡ Emergency hotkey (Ctrl+Alt+G)
- 📊 Process termination

## Installation
```bash
git clone https://github.com/yourusername/ghost-mode.git
cd ghost-mode
pip install -r requirements.txt
```

## Usage
```bash
# Windows (Admin recommended)
python main.py

# Linux (Root required)
sudo python main.py
```

## Building
```bash
pyinstaller --onefile --windowed --icon=icon.ico main.py
```

## Contributing
Pull requests welcome! For major changes, please open an issue first.

## License
[MIT](LICENSE)
