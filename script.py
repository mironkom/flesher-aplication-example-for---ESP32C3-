import os
import threading
import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports
import esptool

def get_com_ports():
    """COM-port list"""
    return [port.device for port in serial.tools.list_ports.comports()]

def flash_firmware():
    # scroll bar list
    port = port_var.get()
    if not port:
        status_label.config(text="Please select COM-port!")
        return

    # button - off and status - burning
    flash_button.config(state=tk.DISABLED)
    status_label.config(text="Burning...")

    # Paths to binary files
    script_dir = os.path.dirname(os.path.abspath(__file__))
    bootloader_path = os.path.join(script_dir, 'bootloader.bin')
    partitions_path = os.path.join(script_dir, 'partitions.bin')
    boot_app0_path  = os.path.join(script_dir, 'boot_app0.bin')
    firmware_path   = os.path.join(script_dir, 'firmware.bin')

    args = [
        '--chip', 'esp32c3',
        '--port', port,
        '--baud', '921600',
        '--before', 'default_reset',
        '--after', 'hard_reset',
        'write_flash', '-z',
        '--flash_mode', 'dio',
        '--flash_freq', '80m',
        '--flash_size', '4MB',
        '0x0000', bootloader_path,
        '0x8000', partitions_path,
        '0xe000', boot_app0_path,
        '0x10000', firmware_path
    ]

    # Start flashing
    try:
        esptool.main(args)
        status_label.config(text="✅ Successfully!")
    except Exception as e:
        status_label.config(text=f"❌ ERROR: {e}")
    finally:
        flash_button.config(state=tk.NORMAL)

def start_flashing():
    # Start flashing in a separate thread
    threading.Thread(target=flash_firmware, daemon=True).start()

# === GUI ===
root = tk.Tk()
root.title("ESP32C3_FLASHER")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Combobox for COM-port selection
ttk.Label(frame, text="Select COM-port:").grid(row=0, column=0, padx=5, pady=5)
port_var = tk.StringVar()
port_combobox = ttk.Combobox(frame, textvariable=port_var, values=get_com_ports(), state="readonly")
port_combobox.grid(row=0, column=1, padx=5, pady=5)

# Set default selection if available
if port_combobox['values']:
    port_combobox.current(0)

# Button "BURN!"
flash_button = ttk.Button(frame, text="BURN!", command=start_flashing)
flash_button.grid(row=1, column=0, columnspan=2, pady=10)

# Status label for button
status_label = ttk.Label(frame, text="Waiting...")
status_label.grid(row=2, column=0, columnspan=2, sticky=tk.W)

root.mainloop()
