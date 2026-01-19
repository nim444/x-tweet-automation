"""Main entry point for X tweet automation."""

import os
from dotenv import load_dotenv

from device import Device
from x_automation import XAutomation


def main():
    # Load environment variables
    load_dotenv()
    device_id = os.getenv("DEVICE_ID", "")

    if not device_id:
        print("Error: DEVICE_ID not set in .env file")
        return

    print(f"Starting automation with device: {device_id}")

    # Connect to device
    device = Device(device_id)
    if not device.connect():
        return

    # Stop all apps
    device.stop_all_apps()

    # Start X automation
    x_auto = XAutomation(device.device)

    # Open X app and composer
    if x_auto.open_x_app():
        x_auto.open_composer()

    print("Automation completed")


if __name__ == "__main__":
    main()
