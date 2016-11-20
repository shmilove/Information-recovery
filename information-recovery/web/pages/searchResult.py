import webapp2
import json

from api.BM25 import BM25


class SearchResult(webapp2.RequestHandler):
    def get(self):
        query = self.request.get('query')
        run_with_stemming = False
        bm = BM25(run_with_stemming)
        if query:
            sorted_bm25_dic = bm.create_bm25_arr(query)

            self.response.write(json.dumps(sorted_bm25_dic))

app = webapp2.WSGIApplication([
    ('/searchResult', SearchResult),
], debug=True)
