import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb
from Db_Structure import *
from EV import *
from datetime import datetime


JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                        extensions=["jinja2.ext.autoescape"],autoescape=True)

class Review(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        Car_reviews = review.query().fetch()
        cars = Electric_Vehicles.query().fetch()
        template_values = {
         "Car_reviews" : Car_reviews,
          "cars" : cars,
          "user" : user
          }
        template = JINJA_ENVIRONMENT.get_template("review.html")
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        template_values = {}
        if user == None:
            template = JINJA_ENVIRONMENT.get_template("error.html")
            template_values["error"] = "Login to access"
            template_values["url"] = users.create_login_url(self.request.uri)
        else:
            rev = review()
            rev.user = user.email()
            rev.car = int(self.request.get('car'))
            car = ndb.Key(Electric_Vehicles,int(self.request.get("car"))).get()
            rev.car_name = car.name
            rev.car_review = self.request.get('review')
            rev.rating = int(self.request.get('rating'))
            rev.date = datetime.now()
            rev.put()
            self.redirect("/")
