@echo off
python -m PyInstaller --onefile ^
    --add-data "bootloader.bin;." ^
    --add-data "partitions.bin;." ^
    --add-data "boot_app0.bin;." ^
    --add-data "firmware.bin;." ^
    --add-data "C:\Users\%username%\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages\esptool\targets\stub_flasher\1\*.json;esptool\targets\stub_flasher\1" ^
    script.py

pause
