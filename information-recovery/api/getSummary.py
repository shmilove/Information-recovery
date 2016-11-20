# -*- coding: utf-8 -*-
from google.appengine.ext.webapp import template
import webapp2
import json

from EncoderUTF8 import UnicodeReader


class GetSummary(webapp2.RequestHandler):
    def get(self):
        movie_serial_num = 0
        movie_path = 7
        movie_name = 2
        summary_id = self.request.get('summary_id')
        if summary_id:
            try:
                csv_file = open('movies.csv', 'r')
                reader = UnicodeReader(csv_file)
                for line in reader:
                    if summary_id == line[movie_serial_num]:
                        movie_file = open(line[movie_path], 'r')
                        movie_summary = movie_file.read().decode("utf-8")
                        self.response.write(json.dumps({'movie_summary': movie_summary, 'movie_name': line[movie_name]}))

                csv_file.close()

            except Exception as e:
                print("Something went wrong with inverted index: " + str(e.message))

        else:
            self.response.write(json.dumps({'status': 'error'}))


app = webapp2.WSGIApplication([
    ('/getSummary', GetSummary),
    # ('/productsCheck', ProductsCheckHandler),
    # ('/finishProducts', ProductFinshListHandler)
], debug=True)
