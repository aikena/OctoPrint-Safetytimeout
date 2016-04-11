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
        self.timer()

    def timer(self):
        run =int(raw_input("Time:  "))
        mins = int(run)
        seconds = 0
        # Loop until we reach time running
        while mins != 0:
        # print "Minutes", mins
            while seconds != 0:
                sys.stdout.write("\r" + str(mins) + ":" +str(seconds))
                sys.stdout.flush()
                time.sleep(1)
                seconds -= 1
        #De-increment minutes 
            sys.stdout.write("\r" + str(mins) + ":" + str(seconds))
            sys.stdout.flush()
            mins -= 1
            seconds =59
        while seconds != 0:
            sys.stdout.write("\r" + str(mins) + ":" +str(seconds))
            sys.stdout.flush()
            time.sleep(1)
            seconds -= 1
        print("This is the state: ")
        print self._printer.is_printing()

 
    def get_settings_defaults(self):
	return dict(Time="0")

    def get_template_configs(self):
        return [
            dict(type="navbar", custom_bindings=False),
            dict(type="settings", custom_bindings=False)
        ]	

   
__plugin_name__ = "Safety Timeout"
__plugin_version__ = "1.0.0"
__plugin_description__ = "A quick \"Safety feature\" After a specified amount of time, this plugin shuts off the temperature of the hotend and the bed"
__plugin_implementation__ = SafetyTimeoutPlugin()
