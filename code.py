import web
import json
from enum import Enum

""" ==============================================================================================
    LET'S (MOSTLY)NOT USE THE TEMPLATES YET. WE CAN REFACTOR ONCE WE HAVE THE BASE DONE. TAKE NEW
    CONCEPTS ONE AT A TIME
============================================================================================== """
render = web.template.render('templates/')

urls = (
    '/', 'index',
    '/thermostats/?', 'deviceList',
    '/thermostats/(\d+)', 'thermostat',
    '/thermostats/(\d+)/test', 'test',
)


class OperatingMode(Enum):
    OFF  = 1
    COOL = 2
    HEAT = 3


class FanMode(Enum):
    AUTO = 1
    ON   = 2


def getUniqueID():
    global uniqueID
    uID = uniqueID
    uniqueID += 1
    return uID


class Database(object):
    def __init__(self, Thermostats):
        self._Thermostats = Thermostats

    @property
    def Thermostats(self):
        return self._Thermostats


class Thermostat(object):
     def __init__(self, ID, Name, OperatingMode):
        self._ID = ID
        self._CurrentTemp = 66

        self.Name = Name
        self.OperatingMode = OperatingMode
        self.FanMode = FanMode.AUTO
        self.SetPoint = None
        self.CoolPoint = None

     @property
     def ID(self):
         return self._ID

     @property
     def CurrentTemp(self):
         return self._CurrentTemp


class index:
    def GET(self, name):
        return render.index(myName)

""" ========================================= GLOBALS ========================================= """

myName = 'Brien'
uniqueID = 0
database = Database([
    Thermostat(getUniqueID(), "Main-Floor Thermostat", FanMode.AUTO),
    Thermostat(getUniqueID(), "Basement Thermostat", FanMode.AUTO)
])

""" ======================================= END GLOBALS ======================================= """


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()


class deviceList:
    def GET(self):
        thermoJSON = [{'name': therm.Name, 'ID': therm.ID} for therm in database.Thermostats]
        web.header('Content-Type', 'application/json')
        return json.dumps(thermoJSON, sort_keys = True, indent = 4)


class thermostat:
    def GET(self, UID):
        thermo = database.Thermostats[int(UID)]
        thermoJSON = {'name': thermo.Name, 'ID': thermo.ID}
        web.header('Content-Type', 'application/json')
        return json.dumps(thermoJSON, sort_keys = True, indent = 4)


class test:
    def GET(self, UID):
        testStr = 'This is a test. Do NOT panic. The thermostat you selected is '
        testStr += database.Thermostats[int(UID)].Name + 'and it is about to go nuclear. I guess \
         it wasn\'t really a test then.\n'
        return testStr
