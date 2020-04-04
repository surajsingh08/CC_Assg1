from google.appengine.ext import ndb

class Electric_Vehicles(ndb.Model):
    name = ndb.StringProperty()
    manufacturer = ndb.StringProperty()
    year = ndb.IntegerProperty()
    battery_size = ndb.FloatProperty()
    wltp_range = ndb.FloatProperty()
    cost = ndb.FloatProperty()
    power = ndb.IntegerProperty()
