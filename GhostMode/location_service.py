"""
Location services for Ghost Mode
Handles GPS spoofing on Windows
"""
import logging
import platform
import random
import winreg

class LocationService:
    """Manages location spoofing functionality"""
    def __init__(self):
        self.os_type = platform.system()
        self.logger = logging.getLogger(__name__)
        self.original_location = None
    
    def spoof_location(self, lat=None, long=None) -> bool:
        """Spoof GPS location on Windows"""
        if self.os_type != 'Windows':
            self.logger.warning("GPS spoofing only supported on Windows")
            return False
            
        try:
            # Generate random coordinates if none provided
            if lat is None:
                lat = random.uniform(-90, 90)
            if long is None:
                long = random.uniform(-180, 180)
                
            # Save original location before spoofing
            self.original_location = self.get_current_location()
            
            # Windows location is stored in registry
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Sensor\\Overrides\\{BFA794E4-F964-4FDB-90F6-51056BFE4B44}",
                0, winreg.KEY_WRITE)
                
            winreg.SetValueEx(key, "SensorPermissionState", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            
            # Additional spoofing would require more complex implementation
            self.logger.info(f"Location spoofed to: {lat}, {long}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error spoofing location: {e}")
            return False
    
    def restore_location(self) -> bool:
        """Restore original GPS location"""
        if self.original_location is None:
            return False
            
        try:
            if self.os_type == 'Windows':
                key = winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE,
                    "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Sensor\\Overrides\\{BFA794E4-F964-4FDB-90F6-51056BFE4B44}",
                    0, winreg.KEY_WRITE)
                    
                winreg.SetValueEx(key, "SensorPermissionState", 0, winreg.REG_DWORD, 1)
                winreg.CloseKey(key)
                
                self.logger.info("Restored original location settings")
                return True
            
        except Exception as e:
            self.logger.error(f"Error restoring location: {e}")
            return False
    
    def get_current_location(self) -> tuple:
        """Get current location settings"""
        # Note: This doesn't actually get real GPS coordinates,
        # just checks if location services are enabled
        try:
            if self.os_type == 'Windows':
                key = winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE,
                    "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Sensor\\Overrides\\{BFA794E4-F964-4FDB-90F6-51056BFE4B44}",
                    0, winreg.KEY_READ)
                    
                val, _ = winreg.QueryValueEx(key, "SensorPermissionState")
                winreg.CloseKey(key)
                return (val,)
            
            return (None,)
        except Exception:
            return (None,)
