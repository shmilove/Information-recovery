#from google.appengine.api import users
from google.appengine.ext.webapp import template

import webapp2


class Search(webapp2.RequestHandler):
     def get(self):
        template_params = {}

        html = template.render("web/templates/search_with_stemming.html", template_params)
        self.response.write(html)


app = webapp2.WSGIApplication([
    ('/search_with_stemming', Search)
], debug=True)
