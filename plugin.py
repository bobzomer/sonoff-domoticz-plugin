# Domoticz Python Plugin for EMS bus Wi-Fi Gateway with Proddy's EMS-ESP firmware
# Author: bobzomer@gmail.com
# https://github.com/bbqkees/ems-esp-domoticz-plugin
# Proddy's EMS-ESP repository: https://github.com/proddy/EMS-ESP
# Product Wiki: https://bbqkees-electronics.nl/wiki/
#
#
"""
<plugin key="sonoff-mini" name="Sonoff Mini" version="0.1">
    <description>
      Plugin to interface with Sonoff Mini devices with official firmware in DIY mode
    </description>
    <params>
        <param field="Address" label="Sonoff Mini IP address" width="300px" required="true" default="10.10.7.1"/>
        <param field="Port" label="Port" width="300px" required="true" default="8081"/>
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="Extra verbose" value="Verbose+"/>
                <option label="Verbose" value="Verbose"/>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal" default="true" />
            </options>
        </param>
    </params>
</plugin>
"""
import Domoticz
import http.client
import json


class Sonoff:
    def __init__(self, host, port):
        self.device_id = ""
        self.host = host
        self.port = port

    def checkDevices(self):
        if 1 not in Devices:
            Domoticz.Debug("Create Main Switch Device")
            Domoticz.Device(Name="EMS thermostat current temp", Unit=1, Type=244, Subtype=73).Create()

    def ask(self, path, **data):
        full_data = {
            "deviceid": self.device_id,
            "data": data
        }
        conn = http.client.HTTPConnection(self.host, self.port)
        conn.request('PUT', path, json.dumps(full_data), headers={'Content-Type': 'application/json'})
        response = conn.getresponse()
        if response.status != 200:
            raise Exception(response.reason)
        ret = response.read()
        if len(ret) == 0:
            return None
        return json.loads(str(ret, encoding='utf8'))

    def switch(self, status):
        self.ask('/zeroconf/switch',  switch="on" if status else "off")

    def onCommand(self, unit, command, level, color):
        Domoticz.Log("onCommand called for Unit " + str(unit) + ": Parameter '" + str(command) + "', Level: " + str(level))

        if unit == 1:
            self.switch(command.lower() == 'on')



class SonoffPlugin:
    def onStart(self):
        self.debugging = Parameters["Mode6"]

        if self.debugging == "Verbose+":
            Domoticz.Debugging(2+4+8+16+64)
        if self.debugging == "Verbose":
            Domoticz.Debugging(2+4+8+16+64)
        if self.debugging == "Debug":
            Domoticz.Debugging(2+4+8)

        self.address = Parameters["Address"].replace(" ", "")
        self.port = int(Parameters["Port"].replace(" ", ""))
        self.controller = Sonoff(self.address, self.port)
        self.controller.checkDevices()

    def checkDevices(self):
        Domoticz.Debug("checkDevices called")

    def onStop(self):
        Domoticz.Debug("onStop called")

    def onCommand(self, Unit, Command, Level, Color):
        Domoticz.Debug("Command: " + Command + " (" + str(Level))
        self.controller.onCommand(Unit, Command, Level, Color)

    def onConnect(self, Connection, Status, Description):
        Domoticz.Debug("onConnect called")

    def onDisconnect(self, Connection):
        Domoticz.Debug("onDisconnect called")

    def onHeartbeat(self):
        Domoticz.Debug("onHeartbeat called")


global _plugin
_plugin = SonoffPlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Color):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Color)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()
    