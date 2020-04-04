from google.appengine.ext import ndb

class Users(ndb.Model):
    email = ndb.StringProperty()
from google.appengine.ext import ndb

class review(ndb.Model):
    user = ndb.StringProperty()
    car = ndb.IntegerProperty()
    car_name = ndb.StringProperty()
    car_review = ndb.StringProperty()
    rating = ndb.IntegerProperty()
    date = ndb.DateTimeProperty()
    
