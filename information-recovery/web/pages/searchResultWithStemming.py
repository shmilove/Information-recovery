import webapp2
import json

from api.runTagger import call_meni
from api.BM25 import BM25


class SearchResultWithStemming(webapp2.RequestHandler):
    def get(self):
        query = self.request.get('query')
        run_with_stemming = True
        bm = BM25(run_with_stemming)
        if query:
            query = call_meni(query.encode('utf-8'))
            sorted_bm25_dic = bm.create_bm25_arr(query)
            self.response.write(json.dumps(sorted_bm25_dic))

app = webapp2.WSGIApplication([
    ('/searchResultWithStemming', SearchResultWithStemming),
], debug=True)
