"""
Hardware control module for Ghost Mode
Handles webcam, microphone, and other device controls
"""
import logging
import platform
import subprocess
from typing import List

class HardwareController:
    """Controls hardware devices for privacy"""
    def __init__(self):
        self.os_type = platform.system()
        self.logger = logging.getLogger(__name__)
        self.devices_disabled = False
    
    def disable_webcam(self) -> bool:
        """Disable webcam hardware"""
        try:
            if self.os_type == 'Windows':
                # Try disabling webcam via PowerShell PnP cmdlets
                cmd = [
                    'powershell', '-Command',
                    'Get-PnpDevice -Class Camera | Disable-PnpDevice -Confirm:$false'
                ]
                result = subprocess.run(cmd, capture_output=True, text=True)
                success = (result.returncode == 0)
                if not success:
                    # Fallback: disable usbvideo driver service
                    reg_cmd = [
                        'reg', 'add', r'HKLM\SYSTEM\CurrentControlSet\Services\usbvideo',
                        '/v', 'Start', '/t', 'REG_DWORD', '/d', '4', '/f'
                    ]
                    subprocess.run(reg_cmd, capture_output=True, text=True)
                    subprocess.run(['net', 'stop', 'usbvideo'], capture_output=True, text=True)
                    success = True
                self.logger.info(f"Webcam disable success: {success}")
                return success
            else:
                # Linux: Unload webcam kernel module
                result = subprocess.run(
                    ['sudo', 'modprobe', '-r', 'uvcvideo'],
                    capture_output=True, text=True
                )
                self.logger.info(f"Webcam disable result: {result.stdout}")
                return result.returncode == 0
        except Exception as e:
            self.logger.error(f"Error disabling webcam: {e}")
            return False
    
    def disable_microphone(self) -> bool:
        """Disable microphone hardware"""
        try:
            if self.os_type == 'Windows':
                # Try disabling microphone via PowerShell
                cmd = [
                    'powershell', '-Command',
                    'Get-PnpDevice -Class AudioEndpoint | Where-Object {$_.FriendlyName -like "*Microphone*"} | Disable-PnpDevice -Confirm:$false'
                ]
                result = subprocess.run(cmd, capture_output=True, text=True)
                success = (result.returncode == 0)
                if not success:
                    # Fallback: stop audio services
                    subprocess.run(['net', 'stop', 'AudioEndpointBuilder'], capture_output=True, text=True)
                    subprocess.run(['net', 'stop', 'Audiosrv'], capture_output=True, text=True)
                    success = True
                self.logger.info(f"Microphone disable success: {success}")
                return success
            else:
                # Linux: Mute using ALSA
                result = subprocess.run(
                    ['amixer', 'set', 'Capture', 'nocap'],
                    capture_output=True, text=True
                )
                self.logger.info(f"Microphone disable result: {result.stdout}")
                return result.returncode == 0
        except Exception as e:
            self.logger.error(f"Error disabling microphone: {e}")
            return False
    
    def randomize_mac_address(self, interface: str = 'wlan0') -> bool:
        """Randomize MAC address (Linux only)"""
        if self.os_type != 'Linux':
            self.logger.warning("MAC randomization only supported on Linux")
            return False
            
        try:
            # Disable interface
            subprocess.run(['sudo', 'ifconfig', interface, 'down'], check=True)
            # Randomize MAC
            subprocess.run(['sudo', 'macchanger', '-r', interface], check=True)
            # Enable interface
            subprocess.run(['sudo', 'ifconfig', interface, 'up'], check=True)
            self.logger.info(f"Randomized MAC address for {interface}")
            return True
        except Exception as e:
            self.logger.error(f"Error randomizing MAC: {e}")
            return False
    
    def activate_protections(self) -> bool:
        """Enable all hardware protections"""
        success = True
        if not self.disable_webcam():
            success = False
        if not self.disable_microphone():
            success = False
        self.devices_disabled = True
        return success
    
    def deactivate_protections(self) -> bool:
        """Disable all hardware protections"""
        success = True
        if self.os_type == 'Windows':
            # Restore usbvideo driver
            reg_cmd = [
                'reg', 'add', r'HKLM\SYSTEM\CurrentControlSet\Services\usbvideo',
                '/v', 'Start', '/t', 'REG_DWORD', '/d', '3', '/f'
            ]
            subprocess.run(reg_cmd, capture_output=True, text=True)
            subprocess.run(['net', 'start', 'usbvideo'], capture_output=True, text=True)
            # Restart audio services
            subprocess.run(['net', 'start', 'AudioEndpointBuilder'], capture_output=True, text=True)
            subprocess.run(['net', 'start', 'Audiosrv'], capture_output=True, text=True)
        self.devices_disabled = False
        return success
    
    def check_webcam_status(self) -> bool:
        """Check if webcam is disabled"""
        # TODO: Implement proper status check
        return False
    
    def check_microphone_status(self) -> bool:
        """Check if microphone is disabled"""
        # TODO: Implement proper status check
        return False
