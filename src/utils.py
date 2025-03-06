import os
import subprocess
import dearpygui.dearpygui as dpg

def reboot(type, isfastboot):
    if type == "Normal" and isfastboot == False: #omfg dearpygui thank you for existing, and being simple to use
        subprocess.run(["adb", "reboot"], capture_output=True)
    elif type == "Recovery" and isfastboot == False:
        subprocess.run(["adb", "reboot", "recovery"], capture_output=True)
    elif type == "Fastboot" and isfastboot == False:
        subprocess.run(["adb", "reboot", "bootloader"], capture_output=True)
    elif type == "EDL" and isfastboot == False:
        subprocess.run(["adb", "reboot", "edl"], capture_output=True)
    
    if type == "Normal" and isfastboot == True:
        subprocess.run(["fastboot", "reboot"], capture_output=True)
    elif type == "Recovery" and isfastboot == True:
        subprocess.run(["fastboot", "reboot", "recovery"], capture_output=True)
    elif type == "Fastboot" and isfastboot == True:
        subprocess.run(["fastboot", "reboot-bootloader"], capture_output=True)
    elif type == "EDL" and isfastboot == True:
        subprocess.run(["fastboot", "reboot", "edl"], capture_output=True) #Not many devices support this, adding in case
    

def get_info(type):
    if type == "state":
        os.system("adb get-state device")
    elif type == "s": #Serial number
        os.system("adb get-serialno")

def restart_adb_server():
    os.system("adb kill-server")
    os.system("adb start-server")

def log_text(output, message):

    dpg.add_text(message, parent=output)
    dpg.set_y_scroll(output, 999999)  # Scroll to bottom

def get_devices(log_window):
    dpg.delete_item("log", children_only=True)
    adb_result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
    devices_list = adb_result.stdout.strip().split("\n")
    fastboot_result = subprocess.run(["fastboot", "devices"], capture_output=True, text=True)
    fastboot_devices_list = fastboot_result.stdout.strip().split("\n")

    for line in devices_list:
        log_text(log_window, line)
    
    for line in fastboot_devices_list:
        log_text(log_window, line)

def shell():
    os.system("adb shell")