# sonoff-domoticz-plugin
Domoticz plugin for the Sonoff Mini with official firmware in DIY mode.

See [http://developers.sonoff.tech/basicr3-rfr3-mini-http-api.html](http://developers.sonoff.tech/basicr3-rfr3-mini-http-api.html). 

# Installation and configuration

## Installing the plugin

1. Ensure your Sonoff Mini is in DIY mode. See [official instructions](http://developers.sonoff.tech/sonoff-diy-mode-api-protocol.html.)
2. Go to the `domoticz/plugins` directory and clone this repository.
3. Restart the domoticz service.

## Using the plugin
Create a new hardware with `Sonoff Mini` type. Specify the IP address of your module. Default port should be OK.
On the first run the plugin will create a new switch device. Switching this device in Domoticz will
update your Sonoff Mini. 

**WARNING:** There will be no reading of status.

## Issues
If you find a problem with the plugin, just open an issue here.
