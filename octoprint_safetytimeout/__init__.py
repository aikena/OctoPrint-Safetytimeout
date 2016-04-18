# coding=utf-8 (test git)

from __future__ import absolute_import
import time 
import octoprint.plugin 
import octoprint.printer 
import sys
import logging
from octoprint.events import eventManager, Events

class SafetyTimeoutPlugin(octoprint.plugin.AssetPlugin,
			  octoprint.plugin.EventHandlerPlugin,
			  octoprint.plugin.StartupPlugin,
			  octoprint.plugin.TemplatePlugin,
			  octoprint.plugin.SettingsPlugin):
	
    def on_after_startup(self):
        self._logger.info("Safety Timeout! (more: %s)" % self._settings.get(["Time"]))

        self.countdown()
	temperatures = self._printer.get_current_temperatures()
        if float(temperatures.get("bed").get("target")) > 0:
            self._logger.info("The Temperature is: %s" % temperatures)
        else:
            self._logger.info("something something something: %s" % temperatures)
	self._logger.info("this is stuff: %s" % temperatures.keys())

    def countdown(self):
	# t comes in as a string from the get.
	t = self._settings.get(["Time"]) 
	# Convert to a number; could be a float.
	t = float(t)
	# Further cast down to an int.
	t = int(t) 
	t = t*60
        while t >= 0:
	    mins, secs = divmod(t, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            sys.stdout.write("\r" + timeformat)
            sys.stdout.flush()
            time.sleep(1)
            t -= 1
        print('Goodbye!\n\n\n\n\n')
  
    def shutdown(self):
	if self._printer.is_printing():
	    #self.timer()
	    print("The printer is printing!")
	else:
	    self._printer.set_temperature("bed", 0)
	    print("Bed temperature set to 0")
	    self._printer.set_temperature("tool0", 0)
	    print("Tool temperature set to 0")
	 
    def get_settings_defaults(self):
	return dict(Time="0")
	print("JELLOOOO")

    def get_template_configs(self):
        return [
            dict(type="navbar", custom_bindings=False),
            dict(type="settings", custom_bindings=False)
        ]	

   
__plugin_name__ = "Safety Timeout"
__plugin_version__ = "1.0.0"
__plugin_description__ = "A quick \"Safety feature\" After a specified amount of time, this plugin shuts off the temperature of the hotend and the bed"
__plugin_implementation__ = SafetyTimeoutPlugin()
