#from google.appengine.api import users
from google.appengine.ext.webapp import template

import webapp2

from urllib import urlopen


class IndexHandler(webapp2.RequestHandler):
     def get(self):
        template_params = {}
        html = urlopen("web/templates/index.html").read()
        self.response.write(html)


app = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/index', IndexHandler)
], debug=True)
