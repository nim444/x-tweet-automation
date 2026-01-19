"""Device connection and management."""

import uiautomator2 as u2
from time import sleep


class Device:
    """Handles Android device connection via ADB."""

    def __init__(self, device_id: str):
        self.device_id = device_id
        self.device = None

    def connect(self):
        """Connect to the Android device."""
        try:
            self.device = u2.connect(self.device_id)
            print(f"Connected to device: {self.device_id}")
            return True
        except Exception as e:
            print(f"Failed to connect to device {self.device_id}: {e}")
            return False

    def stop_all_apps(self):
        """Stop all running apps on the device."""
        if not self.device:
            print("Device not connected")
            return False

        try:
            self.device.app_stop_all()
            sleep(2)
            print("Stopped all apps")
            return True
        except Exception as e:
            print(f"Failed to stop all apps: {e}")
            return False
