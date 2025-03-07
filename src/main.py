import dearpygui.dearpygui as dpg

from utils import * #Almost every single thing it does

#Default values for radio buttons
isfastboot = False
radio = "Normal"

#DearPyGUI initialization stuff
dpg.create_context()
dpg.create_viewport(title="YA ADB/Fastboot GUI", width=450, height=530)
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
#END OF CRAP CODE

#We initialize the buttons and other stuff
with dpg.window(tag="primary"):
    dpg.add_text("Devices functions:", )
    dpg.add_button(label="Get connected devices", callback=lambda: get_devices("log"))
    dpg.add_button(label="Get state of device", callback=lambda: get_info("state", "log"))
    dpg.add_button(label="Get serial number", callback=lambda: get_info("sn", "log"))

    dpg.add_spacer(height=10)
    dpg.add_text("Reboot options:", )
    dpg.add_button(label="Reboot", callback=lambda: reboot(radio, isfastboot)) #We use the data to tell what mode to reboot the phone is
    dpg.add_radio_button(("Normal", "Recovery", "Fastboot", "EDL"), callback=_log_radio, horizontal=True)
    dpg.add_checkbox(label="Is it in fastboot?", callback=_isfastboot)
    dpg.add_spacer(height=10)
    dpg.add_button(label="Unlock bootloader", callback=lambda: unlock("log"))
    dpg.add_button(label="Lock bootloader", callback=lambda: lock("log"))
    dpg.add_spacer(height=50)
    with dpg.child_window(tag="log", width=400, height=200): #Log window
        dpg.add_text("Click some buttons for output!", parent="log") #Added this to greet the user, it's gonna appear once


#Finishing initialization by viewing our window
dpg.show_viewport()
dpg.set_primary_window("primary", True) #Setting it to primary
dpg.start_dearpygui() #Actually starting dearpygui functions

#Destroying when closing :sob:
dpg.destroy_context()