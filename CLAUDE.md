# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

X (Twitter) automation tool using Android UI automation via uiautomator2 and ADB. The project automates interactions with the X mobile app on Android devices.

## Environment Setup

This project uses `uv` for Python package management with Python 3.14.

```bash
# Install dependencies
uv sync

# Run the main script
uv run main.py
```

## Configuration

Environment variables are configured in `.env` (copy from `.env_example`):
- `DEVICE_ID`: ADB device identifier for the target Android device

The `DEVICE_ID` is also duplicated in `main.py` as a global constant - keep both in sync when updating device configuration.

## Architecture

- **main.py**: Entry point for the automation script
- **uiautomator2**: Primary dependency for Android UI automation, enables programmatic control of Android UI elements
- **ADB connectivity**: Requires Android device connected via ADB (USB or wireless)

## Android Device Requirements

The automation requires:
1. Android device with USB debugging enabled
2. Device connected and authorized via ADB
3. X (Twitter) app installed on the device
4. Device ID obtainable via `adb devices`
