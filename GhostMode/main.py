"""
Ghost Mode - System-wide privacy toggle application
"""
import sys
import logging
import ctypes
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QSystemTrayIcon, QMenu, QAction, QMessageBox, QLabel
from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtGui import QIcon, QKeySequence, QPixmap, QPainter, QBrush, QPen
from hardware_control import HardwareController
from process_manager import ProcessManager
from location_service import LocationService
from audit_logger import AuditLogger

def is_admin():
    """Check if running with admin privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

class GhostSignals(QObject):
    """Signals for hotkey events"""
    toggle_requested = pyqtSignal()

class GhostModeApp(QMainWindow):
    """Main application window for Ghost Mode"""
    def __init__(self):
        super().__init__()
        self.ghost_active = False
        self.signals = GhostSignals()
        self.hardware = HardwareController()
        self.process_manager = ProcessManager()
        self.process_manager.load_target_processes('config/target_processes.txt')
        self.location_service = LocationService()
        self.audit_logger = AuditLogger()
        
        if not is_admin():
            QMessageBox.warning(
                self, 
                "Admin Required", 
                "Some features require administrator privileges.\nPlease restart as administrator."
            )
        
        self.init_ui()
        self.setup_tray_icon()
        self.setup_hotkey()
        self.setup_logging()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Ghost Mode")
        self.setGeometry(100, 100, 300, 200)
        
        self.toggle_btn = QPushButton("Activate Ghost Mode", self)
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.clicked.connect(self.toggle_ghost_mode)
        self.toggle_btn.setGeometry(50, 50, 200, 100)
        
        # Location status label
        self.status_label = QLabel("Location: Unknown", self)
        self.status_label.setGeometry(50, 160, 200, 20)
        
    def setup_tray_icon(self):
        """Create system tray icon"""
        self.tray_icon = QSystemTrayIcon(self)
        
        # Use default icon if custom icon doesn't exist
        icon_path = "icon.ico" if os.path.exists("icon.ico") else None
        if icon_path:
            self.tray_icon.setIcon(QIcon(icon_path))
        else:
            # Create a proper default icon
            pixmap = QPixmap(64, 64)
            pixmap.fill(Qt.transparent)
            painter = QPainter(pixmap)
            painter.setBrush(QBrush(Qt.darkGray))
            painter.drawEllipse(8, 8, 48, 48)
            painter.setPen(QPen(Qt.white, 3))
            painter.drawLine(24, 24, 40, 40)
            painter.drawLine(40, 24, 24, 40)
            painter.end()
            self.tray_icon.setIcon(QIcon(pixmap))
            
        tray_menu = QMenu()
        toggle_action = QAction("Toggle Ghost Mode", self)
        toggle_action.triggered.connect(self.toggle_ghost_mode)
        tray_menu.addAction(toggle_action)
        
        quit_action = QAction("Exit", self)
        quit_action.triggered.connect(sys.exit)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
    
    def setup_hotkey(self):
        """Set up emergency hotkey"""
        self.hotkey = QAction(self)
        self.hotkey.setShortcut(QKeySequence("Ctrl+Alt+G"))
        self.hotkey.triggered.connect(self.activate_ghost_mode)
        self.addAction(self.hotkey)
        
    def setup_logging(self):
        """Configure application logging"""
        logging.basicConfig(
            filename='ghost_mode_audit.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    def toggle_ghost_mode(self, state=None):
        """Toggle ghost mode on/off"""
        if state is None:
            state = not self.ghost_active
        if state:
            self.activate_ghost_mode()
            self.toggle_btn.setText("Deactivate Ghost Mode")
        else:
            self.deactivate_ghost_mode()
            self.toggle_btn.setText("Activate Ghost Mode")
        self.ghost_active = state
    
    def activate_ghost_mode(self):
        """Enable all privacy protections"""
        logging.info("Activating Ghost Mode")
        # Hardware protections
        hw_ok = self.hardware.activate_protections()
        # Terminate target processes
        proc_ok = self.process_manager.kill_processes()
        # Spoof location or randomize MAC
        loc_ok = False
        if self.hardware.os_type == 'Windows':
            loc_ok = self.location_service.spoof_location()
        else:
            loc_ok = self.hardware.randomize_mac_address()
        # Show notification
        messages = []
        messages.append(f"Hardware {'disabled' if hw_ok else 'disable failed'}")
        messages.append(f"Processes {'terminated' if proc_ok else 'termination failed'}")
        if self.hardware.os_type == 'Windows':
            messages.append(f"Location {'spoofed' if loc_ok else 'spoof failed'}")
        else:
            messages.append(f"MAC {'randomized' if loc_ok else 'randomize failed'}")
        self.tray_icon.showMessage("Ghost Mode Activated", "\n".join(messages), QSystemTrayIcon.Information)
        # Update location status label
        if self.hardware.os_type == 'Windows':
            loc_state = self.location_service.get_current_location()
            loc_text = 'Off' if loc_state and loc_state[0] == 0 else 'On'
            self.status_label.setText(f"Location: {loc_text}")
        # Audit log activation
        loc_state = self.location_service.get_current_location() if self.hardware.os_type == 'Windows' else ()
        self.audit_logger.log_activation(
            self.process_manager.killed_processes, hw_ok, loc_ok, loc_state
        )
        
    def deactivate_ghost_mode(self):
        """Disable privacy protections"""
        logging.info("Deactivating Ghost Mode")
        # Restore hardware
        hw_ok = self.hardware.deactivate_protections()
        # Restart processes if needed
        proc_ok = self.process_manager.restore_processes()
        # Restore location settings
        loc_ok = False
        if self.hardware.os_type == 'Windows':
            loc_ok = self.location_service.restore_location()
        # Show notification
        messages = []
        messages.append(f"Hardware {'restored' if hw_ok else 'restore failed'}")
        messages.append(f"Processes {'restored' if proc_ok else 'restore failed'}")
        if self.hardware.os_type == 'Windows':
            messages.append(f"Location {'restored' if loc_ok else 'restore failed'}")
        self.tray_icon.showMessage("Ghost Mode Deactivated", "\n".join(messages), QSystemTrayIcon.Information)
        # Update location status label
        if self.hardware.os_type == 'Windows':
            loc_state = self.location_service.get_current_location()
            loc_text = 'Off' if loc_state and loc_state[0] == 0 else 'On'
            self.status_label.setText(f"Location: {loc_text}")
        # Audit log deactivation
        loc_state = self.location_service.get_current_location() if self.hardware.os_type == 'Windows' else ()
        self.audit_logger.log_deactivation(
            [p for p in self.process_manager.target_processes if self.process_manager.is_process_running(p)], hw_ok, loc_ok, loc_state
        )

def main():
    app = QApplication(sys.argv)
    window = GhostModeApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    print("Starting Ghost Mode application...")
    if not is_admin():
        print("Warning: Not running as admin - requesting elevation")
        # Store original script path
        script = os.path.abspath(sys.argv[0])
        params = ' '.join([script] + sys.argv[1:])
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
        except Exception as e:
            print(f"Failed to elevate privileges: {e}")
            sys.exit(1)
    else:
        print("Running with admin privileges")
        app = QApplication(sys.argv)
        window = GhostModeApp()
        window.show()
        sys.exit(app.exec_())
