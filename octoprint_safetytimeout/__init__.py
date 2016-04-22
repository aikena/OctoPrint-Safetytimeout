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
        self._logger.info("Safety Timeout set to: " % self._settings.get(["Time"]))
	# get the temperatures of the tools
	temperatures = self._printer.get_current_temperatures()
<<<<<<< HEAD
<<<<<<< HEAD
        self._logger.info("The Temperature is: %s" % temperatures)
        self._logger.info("this is stuff: %s" % temperatures.keys())
=======
        '''if float(temperatures.get("bed").get("target")) > 0:
            self._logger.info("The Temperature is: %s" % temperatures)
        else:
            self._logger.info("something something something: %s" % temperatures)
	self._logger.info("this is stuff: %s" % temperatures.keys())'''
=======
    	# create a while loop that constantly checks for temperatures when temperatures is an empty dictionary
>>>>>>> 786ee9b386f203255f22587c0539ed08a26852d9
	while temperatures == {}: 
	    temperatures = self._printer.get_current_temperatures()
           # print temperatures #for testing
	#create a while loop that updates temperatures while the bed and tool0 target are 0
	while float(temperatures.get("bed").get("target")) == 0 and float(temperatures.get("tool0").get("target")) == 0:  
	   # print("you are in the second loop") #for testing
	    temperatures = self._printer.get_current_temperatures()
	#print("yay! you did it") # for testing
	#as soon as our temperatures are set, we start our timer (default is 0, user specified)
	self.countdown()  
<<<<<<< HEAD
>>>>>>> 6bfe3bda938265e0b91c4d96e94957860d5bf5aa
=======

	#log to the terminal 
        self._logger.info("The Temperature is: %s" % temperatures)
        self._logger.info("this is stuff: %s" % temperatures.keys())

>>>>>>> 786ee9b386f203255f22587c0539ed08a26852d9

    def countdown(self):
	#TODO if t is 0 (the default), we need to end this function because that means the user did not want a timer set
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
	#check to see if the printer is printing 
	if self._printer.is_printing():
	    print("The printer is printing!")
	    #if the printer is printing we do not want to interupt it 
	else:
	    #else, we need to set the temperature of the bed and the tool to 0 
	    self._printer.set_temperature("bed", 0)
	    print("Bed temperature set to 0")
	    self._printer.set_temperature("tool0", 0)
	    print("Tool temperature set to 0")
	 
    def get_settings_defaults(self):
	#set the default time
	return dict(Time="0")

    def get_template_configs(self):
        return [
           # dict(type="navbar", custom_bindings=False),
            dict(type="settings", custom_bindings=False)
        ]	

   
__plugin_name__ = "Safety Timeout"
__plugin_version__ = "1.0.0"
__plugin_description__ = "A quick \"Safety feature\" After a specified amount of time, this plugin shuts off the temperature of the hotend and the bed as long as the printer is not printing"
__plugin_implementation__ = SafetyTimeoutPlugin()
