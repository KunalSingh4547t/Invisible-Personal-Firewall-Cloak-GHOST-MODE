"""
Unit tests for Ghost Mode application
"""
import unittest
import sys
import os
from unittest.mock import MagicMock, patch

# Import modules to test
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hardware_control import HardwareController
from process_manager import ProcessManager

class TestHardwareController(unittest.TestCase):
    """Test hardware control functionality"""
    
    @patch('platform.system')
    @patch('subprocess.run')
    def test_disable_webcam_windows(self, mock_run, mock_system):
        """Test webcam disable on Windows"""
        mock_system.return_value = 'Windows'
        mock_run.return_value.returncode = 0
        
        hw = HardwareController()
        result = hw.disable_webcam()
        self.assertTrue(result)
        
    @patch('platform.system')
    @patch('subprocess.run')
    def test_disable_webcam_linux(self, mock_run, mock_system):
        """Test webcam disable on Linux"""
        mock_system.return_value = 'Linux'
        mock_run.return_value.returncode = 0
        
        hw = HardwareController()
        result = hw.disable_webcam()
        self.assertTrue(result)
        
    def test_activate_protections(self):
        """Test activating all protections"""
        hw = HardwareController()
        hw.disable_webcam = MagicMock(return_value=True)
        hw.disable_microphone = MagicMock(return_value=True)
        
        result = hw.activate_protections()
        self.assertTrue(result)
        self.assertTrue(hw.devices_disabled)

class TestProcessManager(unittest.TestCase):
    """Test process management functionality"""
    
    @patch('psutil.process_iter')
    def test_kill_processes(self, mock_process_iter):
        """Test process termination"""
        # Create mock processes
        mock_proc1 = MagicMock()
        mock_proc1.info = {'name': 'zoom.exe', 'pid': 123}
        mock_proc2 = MagicMock()
        mock_proc2.info = {'name': 'chrome.exe', 'pid': 456}
        
        mock_process_iter.return_value = [mock_proc1, mock_proc2]
        
        pm = ProcessManager(['zoom.exe', 'chrome.exe'])
        result = pm.kill_processes()
        
        self.assertTrue(result)
        self.assertEqual(len(pm.killed_processes), 2)
        
    def test_load_target_processes(self):
        """Test loading processes from config file"""
        with patch('builtins.open', unittest.mock.mock_open(read_data='zoom.exe\nchrome.exe\n')):
            pm = ProcessManager()
            pm.load_target_processes('dummy_path.txt')
            self.assertEqual(pm.target_processes, ['zoom.exe', 'chrome.exe'])

if __name__ == '__main__':
    unittest.main()
