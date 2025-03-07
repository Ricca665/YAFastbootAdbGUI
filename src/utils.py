import os
import subprocess
import dearpygui.dearpygui as dpg
import asyncio

def log_text(output, message): #Log text to console
    dpg.add_text(message, parent=output)
    dpg.set_y_scroll(output, 999999)  # Scroll to bottom

"""Mess of a code, used to reboot the phone into various modes (for and and fastboot) and also
   hide the output by setting the capture output flag to True, so it tries to print to a variable but it can't
   Since we setted it to tell it to try and print it to the variable and NOT to the console
   I know it's a hacky hack but i don't care as long as it works"""
def reboot(type, isfastboot): 
    if type == "Normal" and isfastboot == False: #omfg dearpygui thank you for existing, and being simple to use
        subprocess.run(["adb", "reboot"], capture_output=True)
    elif type == "Recovery" and isfastboot == False:
        subprocess.run(["adb", "reboot", "recovery"], capture_output=True)
    elif type == "Fastboot" and isfastboot == False:
        subprocess.run(["adb", "reboot", "bootloader"], capture_output=True)
    elif type == "EDL" and isfastboot == False:
        subprocess.run(["adb", "reboot", "edl"], capture_output=True) #Not many devices support this, adding in case
    
    if type == "Normal" and isfastboot == True:
        subprocess.run(["fastboot", "reboot"], capture_output=True)
    elif type == "Recovery" and isfastboot == True:
        subprocess.run(["fastboot", "reboot", "recovery"], capture_output=True)
    elif type == "Fastboot" and isfastboot == True:
        subprocess.run(["fastboot", "reboot-bootloader"], capture_output=True)
    elif type == "EDL" and isfastboot == True:
        subprocess.run(["fastboot", "reboot", "edl"], capture_output=True) #Not many devices support this, adding in case

"""
 Unlocking and locking the bootloader
 I have to capcture both stdout AND stderr, not having realised that fastboot uses both
"""
def unlock(log_window):
    dpg.delete_item("log", children_only=True)
    log_text(log_window, "Trying to unlock bootloader...")
    try:
        result_fastboot_unlock = subprocess.run(["fastboot", "oem", "unlock"], capture_output=True, text=True, timeout=10)
        result = result_fastboot_unlock.stdout.strip().split("\n")
        result_err = result_fastboot_unlock.stderr.strip().split("\n")
        for line in result:
            log_text(log_window, line)

        for line in result_err:
            log_text(log_window, line)
    except subprocess.TimeoutExpired:
        log_text(log_window, "Unable to unlock bootloader... (fastboot command timed out)")


def lock(log_window):
    dpg.delete_item("log", children_only=True)
    log_text(log_window, "Trying to lock bootloader...")
    try:
        result_fastboot_lock = subprocess.run(["fastboot", "oem", "lock"], capture_output=True, text=True, timeout=10)
        result = result_fastboot_lock.stdout.strip().split("\n")
        result_err = result_fastboot_lock.stderr.strip().split("\n")
        for line in result:
            log_text(log_window, line)
            
        for line in result_err:
            log_text(log_window, line)
    except subprocess.TimeoutExpired:
        log_text(log_window, "Unable to lock bootloader... (fastboot command timed out)")

"""End of bootloader unlocking"""

def get_info(type, log_window):
    """Get state, based on type"""
    if type == "state":
        info = subprocess.run(["adb", "get-state", "device"], capture_output=True, text=True)
    elif type == "sn": #Serial number
        info = subprocess.run(["adb", "get-serialno"], capture_output=True, text=True)

    """Print it to log window"""
    dpg.delete_item("log", children_only=True)
    result = info.stdout.strip().split("\n")
    result_err = info.stderr.strip().split("\n")
    for line in result:
        log_text(log_window, line)
        
    for line in result_err:
        log_text(log_window, line)

def restart_adb_server(): #Not implemented, yet...
    os.system("adb kill-server")
    os.system("adb start-server")

def get_devices(log_window): #Get devices both from and and fastboot
    dpg.delete_item("log", children_only=True)
    adb_result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
    devices_list = adb_result.stdout.strip().split("\n")
    fastboot_result = subprocess.run(["fastboot", "devices"], capture_output=True, text=True)
    fastboot_devices_list = fastboot_result.stdout.strip().split("\n")

    for line in devices_list:
        log_text(log_window, line)
    
    for line in fastboot_devices_list:
        log_text(log_window, line)

def shell(): #Not yet implemented...
    os.system("adb shell")