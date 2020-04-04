import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb
from Db_Structure import *
from EV import *

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                        extensions=["jinja2.ext.autoescape"],autoescape=True)

class Compare(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        cars = Electric_Vehicles.query().fetch()
        template_values = { "cars" : cars}
        template = JINJA_ENVIRONMENT.get_template("compare.html")
        self.response.write(template.render(template_values))

    def post(self):
        C1 = self.request.get("car1")
        C2 = self.request.get("car2")
        if C1 == C2:
            template = JINJA_ENVIRONMENT.get_template("error.html")
            template_values = { "error" : "Cannot compare same cars!" , "url" : "compare"}
            self.response.write(template.render(template_values))
        elif  C1 != "" and C2 != "":
            cars = Electric_Vehicles.query().fetch()
            car1 = ndb.Key(Electric_Vehicles,int(C1)).get()
            car2 = ndb.Key(Electric_Vehicles,int(C2)).get()
            template_values = {
             "cars" : cars,
             "car1" : car1,
              "car2" : car2
                }
            template = JINJA_ENVIRONMENT.get_template("compare.html")
            self.response.write(template.render(template_values))
        else:
            template = JINJA_ENVIRONMENT.get_template("error.html")
            template_values = { "error" : "Selecting Two Cars For Comparing!", "url" : "compare"}
            self.response.write(template.render(template_values))
