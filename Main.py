import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb
from Db_Structure import *
from EV import *
from MainPage2 import Page2
from search import *
from Edit import Details
from compare import Compare
from review import Review
from datetime import datetime

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                        extensions=["jinja2.ext.autoescape"],autoescape=True)
class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        url = ""
        url_string = ""
        Message = ""
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            user_key = ndb.Key('Users', user.user_id())
            user_credentials = user_key.get()
            if user_credentials == None:
                Message = "Welcome fellow first time user"
                user_credentials = Users(id = user.user_id())
                user_credentials.email = user.email()
                user_credentials.put()
            else:
                Message = "Welcome back"
            url_string = "logout"
        else:
            url = users.create_login_url(self.request.uri)
            url_string = "login"
        template_values = {
        "url" : url,
        "url_string" : url_string,
        "user" : user,
        "Message" : Message
        }
        template = JINJA_ENVIRONMENT.get_template("Main.html")
        self.response.write(template.render(template_values))
app = webapp2.WSGIApplication([
('/',MainPage),
('/add', Page2),
('/search', Search),
('/details', Details),
('/compare', Compare),
('/review', Review)


])
