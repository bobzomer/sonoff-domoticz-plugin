# sonoff-domoticz-plugin
Domoticz plugin for the Sonoff Mini with official firmware in DIY mode.

See [http://developers.sonoff.tech/basicr3-rfr3-mini-http-api.html](http://developers.sonoff.tech/basicr3-rfr3-mini-http-api.html). 

# Installation and configuration

## Installing the plugin

1. Ensure your Sonoff Mini is in DIY mode. See [official instructions](http://developers.sonoff.tech/sonoff-diy-mode-api-protocol.html.)
2. Go to the `domoticz/plugins` directory
3. Clone this repository : git clone [https://github.com/bobzomer/sonoff-domoticz-plugin](https://github.com/bobzomer/sonoff-domoticz-plugin)
4. Restart the domoticz service.

## Using the plugin
Create a new hardware with `Sonoff Mini` type. Specify the IP address of your module. Default port should be OK.
When the device firmware version < 3.5.0, the device ID can be left blank.
e.g. “Device ID”: “”
When the device firmware version ≥ 3.5.0, the device ID must be filled in.
e.g. “Device ID”: “1000000001”

On the first run the plugin will create a new switch device. Switching this device in Domoticz will update your Sonoff Mini. 

## Issues
If you find a problem with the plugin, just open an issue here.
