# File Structure

```
ghost_mode/
├── main.py              # Entry point and GUI
├── hardware_control.py  # Webcam/mic toggles
├── process_manager.py   # Termination of target processes
├── location_service.py  # Windows location registry toggles
├── audit_logger.py      # Audit log writer
├── ghost_mode.log       # General logs
├── ghost_mode_audit.log # Audit trail
├── config/
│   └── target_processes.txt
├── docs/
│   ├── README.md
│   ├── FILE_STRUCTURE.md
│   ├── SYSTEM_DESIGN.md
│   ├── SOFTWARE_SPECIFICATIONS.md
│   └── SYNOPSIS.md
├── requirements.txt
└── LICENSE
```
