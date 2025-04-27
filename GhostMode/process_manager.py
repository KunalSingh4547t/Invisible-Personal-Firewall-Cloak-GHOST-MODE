"""
Process management for Ghost Mode
Handles terminating and monitoring applications
"""
import logging
import os
import psutil
from typing import List

class ProcessManager:
    """Manages application processes for privacy"""
    def __init__(self, target_processes: List[str] = None):
        self.target_processes = target_processes or []
        self.killed_processes = []
        self.logger = logging.getLogger(__name__)
    
    def load_target_processes(self, file_path: str) -> None:
        """Load target processes from config file"""
        try:
            with open(file_path, 'r') as f:
                self.target_processes = [
                    line.strip() 
                    for line in f.readlines() 
                    if line.strip() and not line.startswith('#')
                ]
            self.logger.info(f"Loaded target processes: {self.target_processes}")
        except Exception as e:
            self.logger.error(f"Error loading target processes: {e}")
    
    def kill_processes(self) -> bool:
        """Terminate all target processes"""
        self.killed_processes = []
        success = True
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'].lower() in [p.lower() for p in self.target_processes]:
                    psutil.Process(proc.info['pid']).terminate()
                    self.killed_processes.append(proc.info['name'])
                    self.logger.info(f"Terminated process: {proc.info['name']}")
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                self.logger.warning(f"Could not terminate process: {e}")
                success = False
        return success
    
    def restore_processes(self) -> None:
        """Attempt to restart killed processes"""
        # TODO: Implement process restoration
        self.logger.info(f"Processes to restore: {self.killed_processes}")
        self.killed_processes = []
    
    def is_process_running(self, process_name: str) -> bool:
        """Check if a specific process is running"""
        try:
            return any(
                proc.info['name'].lower() == process_name.lower()
                for proc in psutil.process_iter(['pid', 'name'])
            )
        except Exception as e:
            self.logger.error(f"Error checking process status: {e}")
            return False
