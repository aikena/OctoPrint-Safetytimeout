from __future__ import absolute_import
import time 
import octoprint.plugin 
import octoprint.printer 
from octoprint.util import RepeatedTimer
import sys
import logging
from octoprint.events import eventManager, Events


class SafetyTimeoutPlugin(octoprint.plugin.AssetPlugin,
			  octoprint.plugin.EventHandlerPlugin,
			  octoprint.plugin.StartupPlugin,
			  octoprint.plugin.TemplatePlugin,
			  octoprint.plugin.SettingsPlugin):	
 
  def condition(self):
    ''' This function is to check and see if the temperature and time are set above 0, and a timer does not already exist.
	If they are: Starts a timer
	If they are not: It does nothing'''
    if self.initialstart == True:
      temperatures = self._printer.get_current_temperatures()
      if int(self._settings.get(["Time"])) > 0 and temperatures != {}:
        if float(temperatures.get("bed").get("target")) != 0 or float(temperatures.get("tool0").get("target")) != 0:
          self.makeTimer()
    return
  
  def makeTimer (self):
    ''' This function creates a timer instance by grabbing the most recent user specified time'''
    self.countdowndefined = True
    self.initial = int(self._settings.get(["Time"]))
    self._logger.info("The Timer Has Been Initiated!")
    seconds = self.initial * 60
    self.countdown = RepeatedTimer(seconds, self.shutdown, run_first=False)
    self.initialstart = False
    self.countdown.start()

  def on_after_startup(self):
    ''' Upon server startup, we define the class variables and create our initial timer that constantly checks to see if a safety timeout is needed '''
    self.countdowndefined = False
    self.initialstart = True
    self.initial = int(self._settings.get(["Time"]))
    self.timer = RepeatedTimer(1.0, self.condition, run_first=True)
    self.timer.start()
  
  def on_settings_save(self, data):
    ''' We overload this function in case someone changes the time after a timer has already been set. It will cancel the old timer, and resume checking to see if another one needs to be created'''
    old_time = self._settings.get(["Time"])
    octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
    new_time = self._settings.get(["Time"])
    if old_time != new_time:
      if self.countdowndefined == True:
        self.countdown.cancel()
        self._logger.info("The Timer Has Been cancelled!")
        seconds = int(new_time) * 60
        self.initialstart = True

  def shutdown(self):
    ''' Checks to see if machine is printing.
	If it is: Resumes checking to see if a timer is needed.
	If it is not: Sets the bed to 0'''
    self.countdown.cancel()
    self.countdowndefined = False
    #check to see if the printer is printing 
    if self._printer.is_printing():
#      print("The printer is printing!")
      self.initialstart = True
#      print("self.countdown has been cancelled")
    #if the printer is printing we do not want to interupt it 
    else:
      #else, we need to set the temperature of the bed and the tool to 0 
      self._printer.set_temperature("bed", 0)
#      print("Bed temperature set to 0")
      self._printer.set_temperature("tool0", 0)
#      print("Tool temperature set to 0")
      self.initialstart = True
#      print("self.countdown has been cancelled")

  def get_settings_defaults(self):
    #set the default time
    return dict(Time="10")

  def get_template_configs(self):
    return [
      dict(type="settings", custom_bindings=False)
    ]

__plugin_name__ = "Safety Timeout"
__plugin_version__ = "1.0.0"
__plugin_description__ = "A quick \"Safety feature\" After a specified amount of time, this plugin shuts off the temperature of the hotend and the bed as long as the printer is not printing"
__plugin_implementation__ = SafetyTimeoutPlugin()
