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
<<<<<<< HEAD
    def get_assets(self):
	    return dict(
			    js=["js/title_status.js"]
			)	

    def on_event(self, event, payload):
	    if event == Events.CLIENT_OPENED:
		    self._plugin_manager.send_plugin_message(self._identifier, self.get_state_id())

    def get_version(self):
	    return self._plugin_version

    def get_update_information(self):
       	    return dict(
		    title_status=dict(
			    displayName="Title Status",
			    displayVersion=self._plugin_version,

			    # version check: github repository
			    type="github_release",
			    user="MoonshineSG",
			    repo="OctoPrint-TitleStatus",
			    current=self._plugin_version,

			    # update method: pip
			    pip="https://github.com/MoonshineSG/OctoPrint-TitleStatus/archive/{target_version}.zip"
		    )
	    )


    def get_state_id(self):
      	try: 
		return self._printer.get_state_id()
	except AttributeError:
		state = self._printer._state
		#see /octoprint/util/comm.py for state values
		if state == None or state == 0:
			return "OFFLINE"
		if state == 4:
			return "CONNECTING"
		if state == 5:
			return "OPERATIONAL"
		if state == 6:
			return "PRINTING"
		if state == 7:
			return "PAUSED"
		if state == 8:
			return "CLOSED"
		if state == 9:
			return "ERROR"
		if state == 10:
			return "CLOSED_WITH_ERROR"
		if state in [1, 2, 3, 11]:
			return "OTHER"
		return "UNKNOWN"
=======
>>>>>>> 52f132c79ddcc292a30a61943691821fc4ca972a
	
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
<<<<<<< HEAD
        stateid = self.get_state_id()
	print(stateid)
        #print self._printer.get_state_id()
=======
        print self._printer.is_printing()
>>>>>>> 52f132c79ddcc292a30a61943691821fc4ca972a

 
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
