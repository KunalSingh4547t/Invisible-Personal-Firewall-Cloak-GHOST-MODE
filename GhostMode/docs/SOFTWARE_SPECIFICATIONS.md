# Software Specifications

Ghost Mode is a desktop Python application providing a one-click privacy lockdown. Below are its detailed software specifications, covering functional and non-functional requirements, interfaces, and validation criteria.

## 1. Functional Requirements

### FR1 – Activation/Deactivation
- FR1.1: Toggle Ghost Mode via GUI button.
- FR1.2: Toggle Ghost Mode via tray menu.
- FR1.3: Toggle via hotkey (Ctrl+Alt+G).

### FR2 – Hardware Controls
- FR2.1: Disable webcam via PowerShell PnP cmdlets on Windows.
- FR2.2: Mute microphone via PnP/service control on Windows.
- FR2.3: Unload webcam module and mute ALSA capture on Linux.

### FR3 – Process Management
- FR3.1: Read `config/target_processes.txt`.
- FR3.2: Terminate matching processes (case-insensitive).
- FR3.3: Track and optionally restore processes.

### FR4 – Location & MAC Spoofing
- FR4.1: Toggle Windows Location Services via registry key.
- FR4.2: Provide current location state (0 or 1).
- FR4.3: Randomize MAC address on Linux using `macchanger`.

### FR5 – Auditing & Logging
- FR5.1: Write detailed entries to `ghost_mode_audit.log`.
- FR5.2: Include timestamp, hardware_ok, location_ok, location_state, and process lists.
- FR5.3: Use `ghost_mode.log` for general INFO/ERROR.

## 2. Non-Functional Requirements

### NFR1 – Usability
- GUI loads within 1 second.
- Notifications appear within 500 ms.

### NFR2 – Performance
- Hardware changes complete within 2 seconds.
- Killing 20 processes within 1 second.

### NFR3 – Reliability & Recoverability
- Partial failures logged, rest of operations proceed.
- Audit logs persist across restarts.

### NFR4 – Security
- Administrative privileges required for hardware/registry operations.
- Warn user if non-admin; disable unsupported features.

### NFR5 – Maintainability
- Single Responsibility Principle for modules.
- Dependencies limited to PyQt5, psutil, pywin32, macchanger.

### NFR6 – Portability
- Runs on Windows 10+ and major Linux distros.
- Detects OS; disables unsupported operations.

## 3. External Interfaces

### User Interface
- Main window: toggle button, status label.
- Tray icon: toggle, exit menu.
- Hotkey listener.

### Hardware/OS API
- Windows registry (`winreg`).
- PowerShell (`Get-PnpDevice`, `Disable-PnpDevice`).
- Linux commands (`modprobe`, `amixer`, `macchanger`).

### Configuration File
- Location: `config/target_processes.txt`.
- Format: one process name per line, ignore comments.

### Logging Files
- `ghost_mode.log` for debug.
- `ghost_mode_audit.log` for audit.

## 4. Validation & Testing

### Unit Tests
- Mock OS calls for hardware and registry.
- Validate process termination logic.
- Verify log entries correct.

### Integration Tests
- End-to-end activation/deactivation on Windows VM.
- Confirm UI elements and tray notifications.

### Acceptance Criteria
- GUI and tray icon appear.
- All functional requirements satisfied under admin.
- Audit entries reflect actions.

## 5. Future Enhancements
- CLI interface for headless use.
- Process restoration implementation.
- macOS support via CoreLocation API.
- Dark mode theme.
