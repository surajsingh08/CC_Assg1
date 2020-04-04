import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb
from Db_Structure import *
from EV import *
JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                        extensions=["jinja2.ext.autoescape"],autoescape=True)

class Details(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        template_values = {}
        if user is None:
            template = JINJA_ENVIRONMENT.get_template("Error.html")
            template_values["error"] = "Login to access"
            template_values["url"] = users.create_login_url(self.request.uri)
            self.response.write(template.render(template_values))
        else:
            key = self.request.get("car")
            car = ndb.Key(Electric_Vehicles,int(key)).get()
            template_values["car"] = car
            template = JINJA_ENVIRONMENT.get_template("Details.html")
            self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        template_values = {}
        key = self.request.get("car")
        ev = ndb.Key(Electric_Vehicles,int(key)).get()
        if self.request.get("button") == "Update":
            ev.name = self.request.get("name")
            ev.manufacturer = self.request.get("manufacturer")
            ev.year = int(self.request.get("year"))
            ev.battery_size = float(self.request.get("battery"))
            ev.wltp_range = float(self.request.get("wltp"))
            ev.cost = float(self.request.get("cost"))
            ev.power = int(self.request.get("power"))
            ev.put()
        elif self.request.get("button") == "Delete":
            ev.key.delete()
        self.redirect("/search")
