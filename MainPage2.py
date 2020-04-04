import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb
from Db_Structure import *
from EV import *
JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                        extensions=["jinja2.ext.autoescape"],autoescape=True)


class Page2(webapp2.RedirectHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        template_values = {}
        if user == None:
            template = JINJA_ENVIRONMENT.get_template("error.html")
            template_values["error"] = "Login to access"
            template_values["url"] = users.create_login_url(self.request.uri)
        else:
            template = JINJA_ENVIRONMENT.get_template("add_EV.html")
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        car = Electric_Vehicles.query(ndb.AND(Electric_Vehicles.name == self.request.get("name"),
                    Electric_Vehicles.manufacturer == self.request.get("manufacturer"),
                    Electric_Vehicles.year == int(self.request.get("year")))).fetch()
        if car == []:
            ev = Electric_Vehicles()
            ev.name = self.request.get("name")
            ev.manufacturer = self.request.get("manufacturer")
            ev.year = int(self.request.get("year"))
            ev.battery_size = float(self.request.get("battery"))
            ev.wltp_range = float(self.request.get("wltp"))
            ev.cost = float(self.request.get("cost"))
            ev.power = int(self.request.get("power"))
            query=Electric_Vehicles.query(ndb.AND(Electric_Vehicles.name==ev.name,Electric_Vehicles.manufacturer==ev.manufacturer,Electric_Vehicles.year==ev.year))
            if query.count()==0:
                ev.put()
            self.redirect("/")
        else:
            template_values = {}
            template = JINJA_ENVIRONMENT.get_template("add_EV.html")
            #template_values["error"] = "Vehicle with the same details already present"
            template_values["url"] = "add"
            template_values["user"] = users.get_current_user()
            self.response.write(template.render(template_values))
