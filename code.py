import web
import json
from enum import Enum

""" ==============================================================================
    LET'S NOT USE THE TEMPLATES YET. WE CAN REFACTOR ONCE WE HAVE THE BASE DONE. TAKE NEW
    CONCEPTS ONE AT A TIME
    ============================================================================== """
render = web.template.render('templates/')

urls = (
    '/', 'index',
    '/thermostat', 'thermo'
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
        # no templates yet
        return render.index(myName)
        # return 'hi'

    def POST(self, name):
        testJSON = { 'name': name, 'swagalicious': 'lishaswagic' }
        web.header('Content-Type', 'application/json')
        return json.dumps(testJSON)

myName = 'Brien'
uniqueID = 0
therm0 = Thermostat(getUniqueID(), "Main-Floor Thermostat", FanMode.AUTO)
therm1 = Thermostat(getUniqueID(), "Basement Thermostat", FanMode.AUTO)


if __name__ == "__main__":
    # global database
    # database = Database(Thermostat(getUniqueID(), "Main floor", FanMode.AUTO))

    app = web.application(urls, globals())
    app.run()


class thermo:
    def GET(self):
        global therm0
        thermoJSON = { 'name': therm0.Name, 'ID': therm0.ID }
        web.header('Content-Type', 'application/json')
        return json.dumps(thermoJSON)



class Database(object):
    def __init__(self, Thermostats):
        self._Thermostats = Thermostats

    @property
    def Thermostats(self):
        return self._Thermostats
