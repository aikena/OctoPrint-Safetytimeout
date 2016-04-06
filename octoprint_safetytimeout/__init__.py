# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin 

class SafetyTimeoutPlugin(octoprint.plugin.StartupPlugin,
			  octoprint.plugin.TemplatePlugin,
			  octoprint.plugin.SettingsPlugin):

    def on_after_startup(self):
        self._logger.info("Safety Timeout! (more: %s)" % self._settings.get(["Time"]))

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
