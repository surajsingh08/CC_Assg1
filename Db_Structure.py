from google.appengine.ext import ndb

class Users(ndb.Model):
    email = ndb.StringProperty()
