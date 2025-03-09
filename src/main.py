import dearpygui.dearpygui as dpg
import subprocess
from utils import * #Almost every single thing it does
import easygui
from zipfile import ZipFile
import urllib.request

#Default values for radio buttons
isfastboot = False
radio = "Normal"
file = ""
partition = "Boot"

#DearPyGUI initialization stuff
dpg.create_context()
dpg.create_viewport(title="YA ADB/Fastboot GUI", width=750, height=700)
dpg.setup_dearpygui()

#RADIO BUTTONS ONLY
#TODO: Rewrite this shit of a radio input :sob:
def _log_radio(sender, app_data, user_data):
    global radio
    radio = app_data
    return radio

def _isfastboot(sender, app_data, user_data):
    global isfastboot
    isfastboot = app_data
    return isfastboot

def _checkpartition(sender, app_data, user_data):
    global partition
    partition = app_data
    return partition

def _get_file(sender, app_data, user_data):
    global file
    file = app_data['file_path_name']
    return file
#END OF CRAP CODE

#File selection window
with dpg.file_dialog(directory_selector=False, show=False, callback=_get_file, tag="img_selector", width=700 ,height=400):
    dpg.add_file_extension(".img")
    dpg.add_file_extension(".*")

#We initialize the buttons and other stuff
with dpg.window(tag="primary"):
    dpg.add_text("ADB & Devices functions:", )
    dpg.add_button(label="Get connected devices", callback=lambda: get_devices("log"))
    dpg.add_button(label="Get state of device", callback=lambda: get_info("state", "log"))
    dpg.add_button(label="Get serial number", callback=lambda: get_info("sn", "log"))
    dpg.add_button(label="Restart ADB Server", callback=lambda: restart_adb_server("log"))
    dpg.add_spacer(height=10)
    dpg.add_text("Reboot options:", )
    dpg.add_button(label="Reboot", callback=lambda: reboot(radio, isfastboot)) #We use the data to tell what mode to reboot the phone is
    dpg.add_radio_button(("Normal", "Recovery", "Fastboot", "EDL"), callback=_log_radio, horizontal=True)
    dpg.add_checkbox(label="Is it in fastboot?", callback=_isfastboot)
    dpg.add_spacer(height=10)
    dpg.add_button(label="Unlock bootloader", callback=lambda: unlock("log"))
    dpg.add_button(label="Lock bootloader", callback=lambda: lock("log"))
    dpg.add_spacer(height=10)
    dpg.add_text("Flashing options:", )
    dpg.add_radio_button(("Boot", "Recovery"), callback=_checkpartition, horizontal=True)
    dpg.add_button(label="Select img file", callback=lambda: dpg.show_item("img_selector"))
    dpg.add_button(label="Flash selected partition", callback=lambda: flash("log", file, partition))

    dpg.add_spacer(height=50)

    with dpg.child_window(tag="log", width=-1, height=200): #Log window
        dpg.add_text("Click some buttons for output!", parent="log") #Added this to greet the user, it's gonna appear once

"""ADB && FASTBOOT CHECK"""
try:
    subprocess.run(["adb"])
    subprocess.run(["fastboot"])
except FileNotFoundError:
    title = "ADB/Fastboot not found!"
    msg = "It sesms like ADB and/or Fastboot is not installed \n Want me to install it for you?"
    if easygui.ynbox(msg, title):     # show a Continue/Cancel dialog
        try:
            if os.name == 'nt': # Windows
                urllib.request.urlretrieve("https://dl.google.com/android/repository/platform-tools-latest-windows.zip", "win.zip")
                with ZipFile("win.zip", 'r') as zip_ref:
                    zip_ref.extractall(".")
                adb_path = os.path.abspath("platform-tools")
                subprocess.run(["setx", "PATH", f"%PATH%;{adb_path}"], shell=True)  # add adb to path permamently
            elif os.name == 'posix': # Mac OS
                urllib.request.urlretrieve("https://dl.google.com/android/repository/platform-tools-latest-darwin.zip", "mac.zip")
                with ZipFile("mac.zip", 'r') as zip_ref:
                    zip_ref.extractall(".")
                                # Detect shell
            else: # UNIX like
                urllib.request.urlretrieve("https://dl.google.com/android/repository/platform-tools-latest-linux.zip", "unix.zip")
                with ZipFile("unix.zip", 'r') as zip_ref:
                    zip_ref.extractall(".")
        except Exception as e:
            easygui.msgbox(title="Error!", msg=f"An error has occured: {e}, Please report it via github issues!")
            exit(0)
    else:
        exit(0)
#Finishing initialization by viewing our window
dpg.show_viewport()
dpg.set_primary_window("primary", True) #Setting it to primary
dpg.start_dearpygui() #Actually starting dearpygui functions

#Destroying when closing :sob:
dpg.destroy_context()