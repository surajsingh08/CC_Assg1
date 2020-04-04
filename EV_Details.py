import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb
from Db_Structure import *
from EV import *

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                        extensions=["jinja2.ext.autoescape"],autoescape=True)

class Ev_Info(webapp2.RedirectHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        car = ndb.Key(Electric_Vehicles,int(self.request.get("car"))).get()
        Car_reviews = review.query(review.car == int(self.request.get("car"))).order(-review.date).fetch()
        avg = 0
        for rev in Car_reviews:
            avg += rev.rating
        if len(Car_reviews) != 0:
            avg = float(avg) / len(Car_reviews)
        else:
            avg = 0
        template_values = { "car" : car, "Car_reviews" : Car_reviews ,"avg_rating" : round(avg,2) }
        template = JINJA_ENVIRONMENT.get_template("EV_Details.html")
        self.response.write(template.render(template_values))
