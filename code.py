import web
import json
import random
from enum import Enum

""" ==============================================================================================
    LET'S (MOSTLY)NOT USE THE TEMPLATES YET. WE CAN REFACTOR ONCE WE HAVE THE BASE DONE. TAKE NEW
    CONCEPTS ONE AT A TIME
============================================================================================== """
render = web.template.render('templates/')

# all calls are idempotent
urls = (
    '/', 'index',
    '/thermostats/?', 'thermostats',
    '/thermostats/(\d+)/?',    'thermostat',
    '/thermostats/(\d+)/id/?',   'thermostatid',
    '/thermostats/(\d+)/temp/?', 'temp',
    '/thermostats/(\d+)/name/?', 'name',
    '/thermostats/(\d+)/name/([A-Za-z0-9\-\_]+)', 'setname',
    '/thermostats/(\d+)/cool/?', 'cool',
    '/thermostats/(\d+)/cool/(\d+)', 'setcool',
    '/thermostats/(\d+)/heat/?', 'heat',
    '/thermostats/(\d+)/heat/(\d+)', 'setheat',
    '/thermostats/(\d+)/fan/?',  'fan',
    '/thermostats/(\d+)/fan/(\d+)',  'setfan',
    '/thermostats/(\d+)/mode/?', 'mode',
    '/thermostats/(\d+)/mode/(\d+)', 'setmode',
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

def getURL(path = None):
    myURL = web.ctx.path
    if path is not None:
        if myURL[len(myURL) - 1] is '/':
            return myURL + path
        else:
            return myURL + '/' + path
    else:
        return myURL

def link(href, method, rel):
    return {'href': href, 'rel': rel, 'method': method }

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
        self.HeatPoint = 62
        self.CoolPoint = 75

     @property
     def ID(self):
         return self._ID

     @property
     def CurrentTemp(self):
         return random.randint(65, 67)


""" ========================================= GLOBALS ========================================= """

uniqueID = 0
database = Database([
    Thermostat(getUniqueID(), "Main-Floor Thermostat", OperatingMode.OFF),
    Thermostat(getUniqueID(), "Basement Thermostat", OperatingMode.OFF),
])

links = {
    'thermostats': '/thermostats',
    'thermostat': '/thermostat/<number>',
    'operatingmode': 'mode',
    'name': 'name',
    'coolpoint': 'cool',
    'heatpoint': 'heat',
    'fanmode': 'fan',
    'currenttemp': 'temp',
    'num': '<num>',
    'id': '<id>',
    'str': '<str>'
}

""" ======================================= END GLOBALS ======================================= """


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()





""" ========================================= HANDLERS ========================================= """


class index:
    def GET(self):
        indexStr = [{ "links": {
                        "href": "/thermostats",
                        "rel": "list",
                        "method": "GET"
                     }}]
        return niceFormat(indexStr)


class thermostats:
    def GET(self):
        thermoJSON = [{
            'name': therm.Name,
            'ID': therm.ID,
            'links': [link(getURL(), 'GET', 'self'), link(getURL(links['id']), 'GET', 'self')]
            } for therm in database.Thermostats]
        return niceFormat(thermoJSON)

    def PUT(self):
        return web.notfound()
    def POST(self):
        return web.notfound()
    def DELETE(self):
        return web.notfound()


class thermostat:
    def GET(self, UID):
        therm = getThermostat(UID)
        if therm is None:
            return web.badrequest('The thermostat ID specified does not exist.')
        else:

            thermoJSON = [{
                'name': therm.Name,
                'ID': therm.ID,
                'CurrentTemp': therm.CurrentTemp,
                'OperatingMode': therm.OperatingMode,
                'CurrentTemp': therm.CurrentTemp,
                'OperatingMode': str(therm.OperatingMode),
                'CoolPoint': therm.CoolPoint,
                'HeatPoint': therm.HeatPoint,
                'FanMode': str(therm.FanMode),
                'links' : [
                    link(getURL(), 'GET', 'self'),
                    link(getURL(links['name']), 'GET', 'self'),
                    link(getURL(links['coolpoint']), 'GET', 'self'),
                    link(getURL(links['heatpoint']), 'GET', 'self'),
                    link(getURL(links['operatingmode']), 'GET', 'self'),
                    link(getURL(links['fanmode']), 'GET', 'self'),
                    link(getURL(links['currenttemp']), 'GET', 'self'),
                    link(getURL(links['operatingmode']), 'GET', 'self'),

                ]
            }]

            return niceFormat(thermoJSON)

    def PUT(self, UID):
        return web.notfound()
    def POST(self, UID):
        return web.notfound()
    def DELETE(self, UID):
        return web.notfound()


class thermostatid:
    def GET(self, UID):
        therm = getThermostat(UID)
        if therm is None:
            return web.badrequest()
        else:
            currentTemp = [{
                'ID': therm.ID,
                'links': [link(getURL(), 'GET', 'self')]
            }]

        return niceFormat(currentTemp)

    def PUT(self, UID):
        return web.notfound()
    def POST(self, UID):
        return web.notfound()
    def DELETE(self, UID):
        return web.notfound()


class temp:
    def GET(self, UID):
        therm = getThermostat(UID)
        if therm is None:
            return web.badrequest()
        else:
            currentTemp = [{
                'currentTemp': therm.CurrentTemp,
                'links': [link(getURL(), 'GET', 'self')]
            }]

        return niceFormat(currentTemp)

    def PUT(self, UID):
        return web.notfound()
    def POST(self, UID):
        return web.notfound()
    def DELETE(self, UID):
        return web.notfound()


class name:
    def GET(self, UID):
        therm = getThermostat(UID)
        if therm is None:
            return web.badrequest()
        else:
            thermStr = [{
                'Name': therm.Name,
                'links': [
                    link(getURL(), 'GET', 'self'),
                    link(getURL(links['str']), 'PUT', 'edit'),
                ]
            }]

            return niceFormat(thermStr)

    def PUT(self, UID):
        return web.notfound()
    def POST(self, UID):
        return web.notfound()
    def DELETE(self, UID):
        return web.notfound()


class setname:
    def PUT(self, UID, name):
        therm = getThermostat(UID)
        if therm is None:
            return web.badrequest()
        else:
            therm.Name = name
            thermStr = [{
                'Name': therm.Name,
                'links': [
                    link(getURL(), 'PUT', 'edit'),
                ]
            }]

            return niceFormat(thermStr)

    def GET(self, UID, name):
        return web.notfound()
    def POST(self, UID, name):
        return web.notfound()
    def DELETE(self, UID, name):
        return web.notfound()


class cool:
    def GET(self, UID):
        therm = getThermostat(UID)
        if therm is None:
            return web.badrequest()
        else:
            coolPoint = [{
                'CoolPoint': therm.CoolPoint,
                'links': [
                    link(getURL(), 'GET', 'self'),
                    link(getURL(links['num']), 'PUT', 'edit')
                ]
            }]

        return niceFormat(coolPoint)

    def PUT(self, UID):
        return web.notfound()
    def POST(self, UID):
        return web.notfound()
    def DELETE(self, UID):
        return web.notfound()


class setcool:
    def PUT(self, UID, temp):
        therm = getThermostat(UID)
        t = int(temp)
        if therm is None or t < 30 or t > 100:
            return web.badrequest()
        else:
            therm.CoolPoint = t
            coolPoint = [{
                'CoolPoint': therm.CoolPoint,
                'links': [ link(getURL(), 'PUT', 'edit') ]
            }]

        return niceFormat(coolPoint)

    def GET(self, UID, temp):
        return web.notfound()
    def POST(self, UID, temp):
        return web.notfound()
    def DELETE(self, UID, temp):
        return web.notfound()

""" ====================================== DONE ====================================== """

class heat:
    def GET(self, UID):
        therm = getThermostat(UID)
        if therm is None:
            return web.badrequest()
        else:
            heatPoint = [{
                'HeatPoint': therm.HeatPoint,
                'links': [
                    link(getURL(), 'GET', 'self'),
                    link(getURL(links['num']), 'PUT', 'edit')
                ]
            }]

        return niceFormat(heatPoint)

    def PUT(self, UID):
        return web.notfound()
    def POST(self, UID):
        return web.notfound()
    def DELETE(self, UID):
        return web.notfound()


class setheat:
    def PUT(self, UID, temp):
        therm = getThermostat(UID)
        t = int(temp)
        if therm is None or t < 30 or t > 100:
            return web.badrequest()
        else:
            therm.HeatPoint = t
            heatPoint = [{
                'HeatPoint': therm.HeatPoint,
                'links': [ link(getURL(), 'PUT', 'edit') ]
            }]

        return niceFormat(heatPoint)

    def GET(self, UID, temp):
        return web.notfound()
    def POST(self, UID, temp):
        return web.notfound()
    def DELETE(self, UID, temp):
        return web.notfound()


class setmode:
    def PUT(self, UID, mode):
        return mode
