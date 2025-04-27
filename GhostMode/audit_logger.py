"""
Audit logging for Ghost Mode
Handles recording of actions for later analysis
"""
import logging

class AuditLogger:
    """Audit logger for Ghost Mode events"""
    def __init__(self, file_path: str = 'ghost_mode_audit.log'):
        self.logger = logging.getLogger('audit')
        # Prevent duplicate handlers
        if not self.logger.handlers:
            handler = logging.FileHandler(file_path)
            handler.setFormatter(
                logging.Formatter('%(asctime)s - %(message)s')
            )
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    def log_activation(self, killed_processes: list, hardware_ok: bool, location_ok: bool, location_state: tuple):
        """Log activated ghost mode actions with hardware, location status, and raw state"""
        status = f"hardware_ok={hardware_ok}, location_ok={location_ok}, location_state={location_state}, terminated={killed_processes}"
        self.logger.info(f"Activated Ghost Mode - {status}")
    
    def log_deactivation(self, running_processes: list, hardware_ok: bool, location_ok: bool, location_state: tuple):
        """Log deactivated ghost mode actions with hardware, location status, and raw state"""
        status = f"hardware_restored={hardware_ok}, location_restored={location_ok}, location_state={location_state}, still_running={running_processes}"
        self.logger.info(f"Deactivated Ghost Mode - {status}")
