# Domoticz Python Plugin for Sonoff Mini DIY mode
# Author: bobzomer@gmail.com
# https://github.com/bobzomer/sonoff-domoticz-plugin.git
"""
<plugin key="sonoff-mini" name="Sonoff Mini" version="0.2" author="Bruno Obsomer"
        externallink="https://sonoff.tech/product/wifi-diy-smart-switches/sonoff-mini">
    <description>
      Plugin to interface with Sonoff Mini devices with official firmware in DIY mode
    </description>
    <params>
        <param field="Address" label="Sonoff Mini IP address" width="300px" required="true" default="10.10.7.1"/>
        <param field="Port" label="Port" width="300px" required="true" default="8081"/>
        <param field="Mode1" label="Device ID" width="300px" required="false" default=""/>
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

class DeviceIds:
    MAIN_SWITCH = 1

class Sonoff:
    def __init__(self, host, port, device_id):
        self.device_id = device_id
        self.host = host
        self.port = port

    def checkDevices(self):
        if DeviceIds.MAIN_SWITCH not in Devices:
            Domoticz.Debug("Create Main Switch Device")
            Domoticz.Device(Name="Main Switch Device", Unit=DeviceIds.MAIN_SWITCH, Type=244, Subtype=73).Create()

    def ask(self, path, **data):
        full_data = {
            "deviceid": self.device_id,
            "data": data
        }
        conn = http.client.HTTPConnection(self.host, self.port)
        conn.request('POST', path, json.dumps(full_data), headers={'Content-Type': 'application/json'})
        response = conn.getresponse()
        if response.status != 200:
            raise Exception(response.reason)
        ret = response.read()
        if len(ret) == 0:
            return None
        return json.loads(str(ret, encoding='utf8'))

    def switch(self, status):
        status_str = "on" if status else "off"
        self.ask('/zeroconf/switch', switch=status_str)
        Devices[DeviceIds.MAIN_SWITCH].Update(nValue=1 if status else 0, sValue=status_str)

    def onCommand(self, unit, command, level, color):
        Domoticz.Log("onCommand called for Unit " + str(unit) + ": Parameter '" + str(command) + "', Level: " + str(level))

        if unit == DeviceIds.MAIN_SWITCH:
            self.switch(command.lower() == 'on')

    def device_status(self):
        result = self.ask('/zeroconf/info', data="")
        status_str = result["data"]["switch"] 
        status=1 if status_str == 'on' else 0
        UpdateDevice(DeviceIds.MAIN_SWITCH, status, status_str)


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
        self.device_id = Parameters["Mode1"].replace(" ", "")
        self.controller = Sonoff(self.address, self.port, self.device_id)
        self.controller.checkDevices()

    def checkDevices(self):
        Domoticz.Debug("checkDevices called")

    def onStop(self):
        Domoticz.Debug("onStop called")

    def onCommand(self, Unit, Command, Level, Color):
        Domoticz.Debug("Command: " + Command + " (" + str(Level))
        try:
            self.controller.onCommand(Unit, Command, Level, Color)
        except Exception as exc:
            Domoticz.Error("Error on command " + Command + " to unit " + str(Unit) + ": " + str(exc))

    def onConnect(self, Connection, Status, Description):
        Domoticz.Debug("onConnect called")

    def onDisconnect(self, Connection):
        Domoticz.Debug("onDisconnect called")

    def onHeartbeat(self):
        Domoticz.Debug("onHeartbeat called")
        self.controller.device_status()

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
    
def UpdateDevice(Unit, nValue, sValue, TimedOut=0, AlwaysUpdate=False):
    if Unit in Devices:
        if (
            Devices[Unit].nValue != nValue
            or Devices[Unit].sValue != sValue
            or Devices[Unit].TimedOut != TimedOut
            or AlwaysUpdate
        ):
            Devices[Unit].Update(nValue=nValue, sValue=str(sValue), TimedOut=TimedOut)
            Domoticz.Debug(
                "Update "
                + Devices[Unit].Name
                + ": "
                + str(nValue)
                + " - '"
                + str(sValue)
                + "'"
            )
