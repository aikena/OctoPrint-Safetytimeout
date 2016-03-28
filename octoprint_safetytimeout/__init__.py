# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin

class SafetyTimeoutPlugin(octoprint.plugin.StartupPlugin,
			  octoprint.plugin.TemplatePlugin,
			  octoprint.plugin.SettingsPlugin):
    def on_after_startup(self):
        self._logger.info("Safety Timeout!!!")

    def get_settings_defaults(self):
	return dict(time= " ")

	

__plugin_name__ = "Safety Timeout"
__plugin_version__ = "1.0.0"
__plugin_description__ = "A quick \"Hello World\" After a specified amount of time, this plugin shuts off the temperature of the hotend and the bed"
__plugin_implementation__ = SafetyTimeoutPlugin()
