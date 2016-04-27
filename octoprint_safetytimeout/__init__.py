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
#  def start(self):
#    print ("Start: %s" % self.initialstart)
#    return self.initialstart

#  def go(self):
#    print ("GO: %s" % self.timerstart)
#    return self.timerstart

 
  def condition(self):
    if self.initialstart == True:
      temperatures = self._printer.get_current_temperatures()
      if float(self._settings.get(["Time"])) > 0 and self._printer.get_current_temperatures() != {}:
        if float(temperatures.get("bed").get("target")) != 0 or float(temperatures.get("tool0").get("target")) != 0:
          self.makeTimer()
	  return
      print("Conditions not met")
    else:
      print("Conditions not met") 	 
  
  def makeTimer (self):
    self.initial = float(self._settings.get(["Time"]))
    self._logger.info("The Timer Has Been Initiated!")
    seconds = self.initial * 60
    print("There are %s seconds left" % seconds)
    self.countdown = RepeatedTimer(seconds, self.shutdown, run_first=False)
    self.initialstart = False
#    self.timerstart = True
    self.countdown.start()

  def on_after_startup(self):
    self.initialstart = True
#    self.timerstart = True
    self.initial = float(self._settings.get(["Time"]))
    #self._logger.info("\n\nSafety Timeout set to: Version {1}, {0}\n\n".format(self._settings.get(["Time"]), self.version))
    self.timer = RepeatedTimer(1.0, self.condition, run_first=True)
    self.timer.start()
    print("Octoprint team")
    # get the temperatures of the tools
    #temperatures = self._printer.get_current_temperatures()
    #self._logger.info("The Temperature is: %s" % temperatures)
    #self._logger.info("this is stuff: %s" % temperatures.keys())
  
#  def countdown(self):
    #TODO if t is 0 (the default), we need to end this function because that means the user did not want a timer set
    # t comes in as a string from the get.
#    t = self._settings.get(["Time"]) 
    # Convert to a number; could be a float.
#    t = float(t)
    # Further cast down to an int.
#    t = int(t) 
#    t = t*60
#    while t >= 0:
#      mins, secs = divmod(t, 60)
#      timeformat = '{:02d}:{:02d}'.format(mins, secs)
#      sys.stdout.write("\r" + timeformat)
#      sys.stdout.flush()
#      time.sleep(1)
#      t -= 1
#      print('Goodbye!\n\n\n\n\n')
  
  def shutdown(self):
    #check to see if the printer is printing 
    if self._printer.is_printing():
      print("The printer is printing!")
#      self.timerstart = False
      self.initialstart = True
      print("self.countdown has been cancelled")
    #if the printer is printing we do not want to interupt it 
    else:
      #else, we need to set the temperature of the bed and the tool to 0 
      self._printer.set_temperature("bed", 0)
      print("Bed temperature set to 0")
      self._printer.set_temperature("tool0", 0)
      print("Tool temperature set to 0")
#      self.timerstart = False
      self.initialstart = True
      print("self.countdown has been cancelled")

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
