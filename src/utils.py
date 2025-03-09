import os
import subprocess
import dearpygui.dearpygui as dpg

"""This is basically the backend
   I am gonna optimize this eventually, the reason i put all of the functions in here is so that
   main.py doesn't contain 1328491 lines of code lmao"""

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
 I have to capcture both stdout AND stderr, because fastboot uses both
"""
def unlock(log_window):
    dpg.delete_item("log", children_only=True)
    log_text(log_window, "Trying to unlock bootloader...")
    try:
        result_fastboot_unlock = subprocess.run(["fastboot", "flashing", "unlock"], capture_output=True, text=True, timeout=10)
        result = result_fastboot_unlock.stdout.strip().split("\n")
        result_err = result_fastboot_unlock.stderr.strip().split("\n")
        for line in result:
            log_text(log_window, line)

        for line in result_err:
            log_text(log_window, line)
    except subprocess.TimeoutExpired:
        log_text(log_window, "Unable to unlock bootloader... Trying different command... (Try 1/2)")

    try:
        result_fastboot_unlock = subprocess.run(["fastboot", "oem", "unlock"], capture_output=True, text=True, timeout=10)
        result = result_fastboot_unlock.stdout.strip().split("\n")
        result_err = result_fastboot_unlock.stderr.strip().split("\n")
        for line in result:
            log_text(log_window, line)

        for line in result_err:
            log_text(log_window, line)
    except subprocess.TimeoutExpired:
        log_text(log_window, "Failed to unlock bootloader... (Timed out!)")


def lock(log_window):
    dpg.delete_item(log_window, children_only=True)
    log_text(log_window, "Trying to lock bootloader...")
    try:
        result_fastboot_lock = subprocess.run(["fastboot", "flashing", "lock"], capture_output=True, text=True, timeout=10)
        result = result_fastboot_lock.stdout.strip().split("\n")
        result_err = result_fastboot_lock.stderr.strip().split("\n")
        for line in result:
            log_text(log_window, line)
            
        for line in result_err:
            log_text(log_window, line)
    except subprocess.TimeoutExpired:
        log_text(log_window, "Failed to lock bootloader... Trying different command... (Try 1/2)")

    try:
        result_fastboot_lock = subprocess.run(["fastboot", "oem", "lock"], capture_output=True, text=True, timeout=10)
        result = result_fastboot_lock.stdout.strip().split("\n")
        result_err = result_fastboot_lock.stderr.strip().split("\n")
        for line in result:
            log_text(log_window, line)
            
        for line in result_err:
            log_text(log_window, line)
    except subprocess.TimeoutExpired:
        log_text(log_window, "Failed to lock bootloader... (Timed out!)")

"""End of bootloader unlocking"""

def flash(log_window, file, partition_input):
    """Flash partition based on file and partition
       I don't take responsability if device goes kaboom"""
    dpg.delete_item(log_window, children_only=True) #Delete log
    
    partition = str(partition_input).lower()
    log_text(log_window, f"Flashing {partition} partition with {file}...")
    #print(partition)
    try:
        flash = subprocess.run(["fastboot", "flash", partition, file], capture_output=True, text=True, timeout=10)
        result = flash.stdout.strip().split("\n")
        result_err = flash.stderr.strip().split("\n")
        for line in result:
            log_text(log_window, line)
            
        for line in result_err:
            log_text(log_window, line)
        log_text(log_window, f"Flashed {partition} partition! Check log for errors")
    except subprocess.TimeoutExpired:
        log_text(log_window, f"Failed to flash {partition} partition... (Timed out!)")

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

def restart_adb_server(log_window): #Not implemented, yet...
    dpg.delete_item("log", children_only=True)
    log_text(log_window, "Killing adb server...")
    subprocess.run(["adb", "kill-server"], capture_output=True, text=True)
    log_text(log_window, "Starting adb server...")
    start_srv = subprocess.run(["adb", "start-server"], capture_output=True, text=True)
    start_srv = start_srv.stdout.strip().split("\n")
    for line in start_srv:
        log_text(log_window, line)

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