# Ghost Mode

Ghost Mode is a Python-based desktop application that provides a single-click privacy lockdown for your system. It disables webcams, microphones, and terminates selected applications, spoofs location services on Windows, and randomizes MAC addresses on Linux. All actions are logged in an audit trail for compliance and forensics.

## Features
- Disable/restore webcam & microphone
- Terminate & optionally restore target processes
- Spoof or toggle location services (Windows)
- Randomize MAC address (Linux)
- System tray icon & global hotkey (Ctrl+Alt+G)
- Comprehensive audit logging

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/aksaayyy/Ghost.git
   cd Ghost/ghost_mode
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run with administrator/root privileges:
   ```bash
   python main.py
   ```

## Usage
- Click **Activate Ghost Mode** to enter privacy lockdown.
- Click **Deactivate Ghost Mode** to restore settings.
- Use **Ctrl+Alt+G** hotkey to toggle.

## Contribution
See [`CONTRIBUTING.md`](../CONTRIBUTING.md) for guidelines.

## License
MIT License. See `LICENSE` file.
