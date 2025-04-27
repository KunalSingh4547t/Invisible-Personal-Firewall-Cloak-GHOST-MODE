# System Design

The Ghost Mode application is architected as a modular, layered system that cleanly separates user interface, core logic, hardware/control services, and persistence/auditing. By isolating each concern into its own component, the design maximizes maintainability, testability, and extensibility, while ensuring that platform-specific complexity is encapsulated.

## 1. Overall Architecture
Ghost Mode follows a classic three-layered architecture plus an independent utilities layer:
- **Presentation Layer** (GUI & Hotkey Manager)
- **Application Layer** (Controller / Orchestrator)
- **Service Layer** (HardwareController, ProcessManager, LocationService, AuditLogger)
- **Infrastructure Layer** (Configuration, Logging, OS APIs)

## 2. Presentation Layer
- **PyQt5 GUI**: A main window hosting a toggle button and status label, plus system tray integration via `QSystemTrayIcon`.
- **Emergency Hotkey**: Implemented with Qt `QAction` and `QKeySequence` (Ctrl+Alt+G).
- **User Feedback**: Notifications via tray icon and status label updates.

## 3. Application Layer
The `GhostModeApp` controller coordinates workflow:
1. Checks admin privileges.
2. Invokes hardware protections, process termination, and location spoofing.
3. Aggregates results for notifications and audit logging.
4. Maintains application state and updates UI elements.

## 4. Service Layer
1. **HardwareController**: Disables/restores webcam & microphone (PowerShell PnP cmdlets on Windows, kernel modules and ALSA on Linux).
2. **ProcessManager**: Reads `config/target_processes.txt`, kills processes via `psutil`, tracks terminated PIDs.
3. **LocationService**: Toggles Windows Location Services via registry; provides current state.
4. **AuditLogger**: Records activation/deactivation events with timestamps, status flags, and process lists.
5. **Configuration Reader**: Loads plaintext file, ignores comments.

## 5. Infrastructure Layer
- **Configuration**: Plain-text process list in `config/`.
- **Logging**: Python `logging` for generic and audit logs.
- **OS Interaction**: Abstracted via `subprocess` and `winreg`.

## 6. Data & Control Flow
1. **Activation**: UI → Controller → Hardware → Process → Location → Audit.
2. **Deactivation**: Reverse sequence restoring components.
3. **Hotkey**: Bypasses UI, directly triggers activation.

## 7. Extensibility & Testability
- Modular services facilitate unit testing by mocking OS calls.
- New services (e.g., VPN, firewall) can be added under Service Layer.

## 8. Security & Privileges
- Warns if not running as admin; requires elevation for sensitive operations.
- Audit logs enable forensics without exposing personal data.

## 9. Packaging & Deployment
- Designed for PyInstaller packaging.
- Fully documented with README, CONTRIBUTING, and license.
