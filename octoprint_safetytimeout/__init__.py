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
    if self.initialstart == True:
      temperatures = self._printer.get_current_temperatures()
      if int(self._settings.get(["Time"])) > 0 and temperatures != {}:
        if float(temperatures.get("bed").get("target")) != 0 or float(temperatures.get("tool0").get("target")) != 0:
          self.makeTimer()
	  return
#      print("Conditions not met")
#    else:
#      print("Conditions not met") 	 
  
  def makeTimer (self):
    self.initial = int(self._settings.get(["Time"]))
    self._logger.info("The Timer Has Been Initiated!")
    seconds = self.initial * 60
#    print("There are %s seconds left" % seconds)
    self.countdown = RepeatedTimer(seconds, self.shutdown, run_first=False)
    self.initialstart = False
    self.countdown.start()

  def on_after_startup(self):
    self.initialstart = True
    self.initial = int(self._settings.get(["Time"]))

    self.timer = RepeatedTimer(1.0, self.condition, run_first=True)
    self.timer.start()
    # get the temperatures of the tools
 

  def shutdown(self):
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
