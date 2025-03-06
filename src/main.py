import os
import dearpygui.dearpygui as dpg

from utils import *

isfastboot = False
radio = "Normal"

dpg.create_context()

dpg.create_viewport(title="YA ADB/Fastboot GUI", width=500, height=500)

dpg.setup_dearpygui()

def _log_radio(sender, app_data, user_data):
    global radio
    radio = app_data
    return radio

def _isfastboot(sender, app_data, user_data):
    global isfastboot
    isfastboot = app_data
    return isfastboot

with dpg.window(tag="primary"):
    dpg.add_text("Devices functions:", )
    dpg.add_button(label="Get connected devices", callback=lambda: get_devices("log"))

    dpg.add_spacer(height=10)
    dpg.add_text("Reboot options:", )
    dpg.add_button(label="Reboot", callback=lambda: reboot(radio, isfastboot))
    dpg.add_radio_button(("Normal", "Recovery", "Fastboot", "EDL"), callback=_log_radio, horizontal=True)
    dpg.add_checkbox(label="Is in fastboot?", callback=_isfastboot)
   
    with dpg.child_window(tag="log", width=400, height=200):
        pass  # empty log window

dpg.show_viewport()
dpg.set_primary_window("primary", True)
dpg.start_dearpygui()
dpg.destroy_context()