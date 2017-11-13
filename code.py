import web
import json
from enum import Enum

""" ==============================================================================================
    LET'S (MOSTLY)NOT USE THE TEMPLATES YET. WE CAN REFACTOR ONCE WE HAVE THE BASE DONE. TAKE NEW
    CONCEPTS ONE AT A TIME
============================================================================================== """
render = web.template.render('templates/')

# all calls are idempotent
urls = (
    '/', 'index',                               # GET only
    '/thermostats/?', 'deviceList',             # GET only
    '/thermostats/(\d+)/?',    'thermostat',    # GET only
    '/thermostats/(\d+)/id',   'thermostatid',  # GET only
    '/thermostats/(\d+)/temp', 'temp',          # GET only
    '/thermostats/(\d+)/name', 'name',        # GET, PUT
    '/thermostats/(\d+)/name/([A-Za-z0-9\-\_]+)', 'setname',  # PUT
    '/thermostats/(\d+)/mode', 'mode',          # GET, PUT
    '/thermostats/(\d+)/cool', 'cool',          # GET, PUT
    '/thermostats/(\d+)/heat', 'heat',          # GET, PUT
    '/thermostats/(\d+)/fan',  'fan',           # GET, PUT
)


class OperatingMode(Enum):
    OFF  = 1
    COOL = 2
    HEAT = 3


class FanMode(Enum):
    AUTO = 1
    ON   = 2

def niceFormat(ajson):
    return json.dumps(ajson, sort_keys = True, indent = 4)

def getUniqueID():
    global uniqueID
    uID = uniqueID
    uniqueID += 1
    return uID

def getThermostat(UID):
    return next((therm for therm in database.Thermostats if therm.ID == int(UID)), None)

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

def link(href, rel, method):
    return {'href': href, 'rel': rel, 'method': method }

class index:
    def GET(self):
        indexStr = [{ "links": {
                        "href": "/thermostats",
                        "rel": "list",
                        "method": "GET"
                     }}]
        # return json.dumps(indexStr, sort_keys = True, indent = 4)
        return niceFormat(indexStr)
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
        return niceFormat(thermoJSON)


class thermostat:
    def GET(self, UID):
        thermo = database.Thermostats[int(UID)]
        thermoJSON = {'name': thermo.Name, 'ID': thermo.ID }
        web.header('Content-Type', 'application/json')
        return niceFormat(thermoJSON)


class temp:
    def GET(self, UID):
        therm = getThermostat(UID)
        if therm is None:
            return web.badrequest('The thermostat ID specified does not exist.')
        else:
            testStr = 'This is a test. Do NOT panic. The thermostat you selected is '
            testStr += therm.Name + ' and it is about to go nuclear. I guess \
             it wasn\'t really a test then.\n'

        return testStr


class name:
    def GET(self, UID):
        return 'GET on name\n'

class setname:
    def PUT(self, UID, name):
        return 'PUT on name. Value provided is ' + name + '\n'
