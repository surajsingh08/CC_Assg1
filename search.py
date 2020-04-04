import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb
from Db_Structure import *
from EV import *
JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                        extensions=["jinja2.ext.autoescape"],autoescape=True)

class Search(webapp2.RedirectHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template("search.html")
        self.response.write(template.render())

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        Queries_String = self.request.get('string_filter')

        Category = self.request.get('category')
        if Category in ("battery", "wltp", "cost") and self.request.get('MIN') != "" and self.request.get('MAX') != "":
            Queries_MIN = float(self.request.get('MIN'))
            Queries_MAX = float(self.request.get('MAX'))
        elif Category in ("year", "power") and self.request.get('MIN') != "" and self.request.get('MAX') != "":
            Queries_MIN = int(self.request.get('MIN'))
            Queries_MAX = int(self.request.get('MAX'))
        car = []
        if Queries_String != "" and Category != "" and self.request.get('MIN') != "" and self.request.get('MAX') != "":
            car = Electric_Vehicles.query(ndb.AND(ndb.OR(Electric_Vehicles.name == Queries_String,
                                            Electric_Vehicles.manufacturer == Queries_String),
                                            ndb.AND(getattr(Electric_Vehicles, Category) >= Queries_MIN,
                                            getattr(Electric_Vehicles, Category) <= Queries_MAX
                                            ))).fetch()
        elif Queries_String != "":
            car = Electric_Vehicles.query(ndb.OR(ndb.OR(Electric_Vehicles.name == Queries_String,
                                            Electric_Vehicles.manufacturer == Queries_String),
                                           )).fetch()
        elif Category != "" and self.request.get('MIN') != "" and self.request.get('MAX') != "":
            car = Electric_Vehicles.query(ndb.AND(getattr(Electric_Vehicles, Category) >= Queries_MIN,
                                        getattr(Electric_Vehicles, Category) <= Queries_MAX
                                        )).fetch()
        else:
            car = Electric_Vehicles.query().fetch()
        template = JINJA_ENVIRONMENT.get_template("Search.html")
        template_values = {}
        template_values["cars"] = car
        self.response.write(template.render(template_values))
