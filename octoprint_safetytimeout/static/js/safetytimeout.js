/*
 * View model for OctoPrint-Safetytimeout
 *
 * Author: Kristian Toole
 * License: AGPLv3
 */
$(function() {
    function SafetytimeoutViewModel(parameters) {
        var self = this;

        // assign the injected parameters, e.g.:
        // self.loginStateViewModel = parameters[0];
        // self.settingsViewModel = parameters[1];

        // TODO: Implement your plugin's view model here.
    }

    // view model class, parameters for constructor, container to bind to
    OCTOPRINT_VIEWMODELS.push([
        SafetytimeoutViewModel,

        // e.g. loginStateViewModel, settingsViewModel, ...
        [ /* "loginStateViewModel", "settingsViewModel" */ ],

        // e.g. #settings_plugin_safetytimeout, #tab_plugin_safetytimeout, ...
        [ /* ... */ ]
    ]);
});
