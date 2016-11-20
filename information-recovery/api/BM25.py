# -*- coding: utf-8 -*-
import operator

from api.EncoderUTF8 import UnicodeReader

__author__ = 'Ilya and Tzuria'


class BM25:

    movies_stop_words = {}
    terms_in_document = {}
    idf_dic = {}
    tf_dic = {}
    movies_name_dic = {}
    movies_link_dic = {}
    run_with_stemming = False

    def __init__(self, run_with_stemming):
        self.initialize_dic()
        self.create_movies_name_dic()
        self.run_with_stemming = run_with_stemming
        doc_len = 0
        for document in self.terms_in_document.keys():
            doc_len += float(self.terms_in_document[document])
        self.avdl = doc_len / len(self.terms_in_document.keys())

    def create_bm25_arr(self, query):
        query_words = self.remove_stop_words(query)
        bm25_dic = {}
        for word in query_words:
            if word in self.tf_dic.keys():
                for doc in self.tf_dic[word].keys():
                    bm25_dic[doc] = self.bm25(query_words, doc)
        result_doc_and_name = []
        if bm25_dic:
            sorted_bm25_dic = sorted(bm25_dic.items(), key=operator.itemgetter(1), reverse=True)

            if len(sorted_bm25_dic) > 0:
                if len(sorted_bm25_dic) > 20:
                    bm25_size = 20
                else:
                    bm25_size = len(sorted_bm25_dic)

                for key in sorted_bm25_dic and range(0, bm25_size):
                    temp_arr = []
                    temp_arr.append(sorted_bm25_dic[key][0])
                    temp_arr.append(self.movies_name_dic[sorted_bm25_dic[key][0]])
                    temp_arr.append(self.movies_link_dic[sorted_bm25_dic[key][0]])
                    result_doc_and_name.append(temp_arr)
                    # result_doc_and_name[sorted_bm25_dic[key][0]] = self.movies_name_dic[sorted_bm25_dic[key][0]]
        return result_doc_and_name

    def bm25(self, query, doc):
        k = 3
        b = 0.5
        sum = 0
        for word in query:
            if word not in self.tf_dic.keys():
                continue
            if doc in self.tf_dic[word].keys():
                TF = float(self.tf_dic[word][doc])
                if doc in self.terms_in_document:
                    len_doc = int(self.terms_in_document[doc])
                else:
                    len_doc = 0
                sum += float(self.idf_dic[word])*TF*(k + 1)/(TF + k*(1 - b + b*(len_doc/self.avdl)))
        return sum

    def remove_stop_words(self, query):
        query = query.replace(",", "").replace('(', '').replace(')', '').replace('.', '').replace('"', '')\
            .replace('?', '').replace('!', '')

        query_words = query.split()
        indexes_to_del = []
        for i in range(0, len(query_words) - 1):
            if query_words[i] in self.movies_stop_words.keys():
                indexes_to_del.append(i)

        indexes_to_del.reverse()
        for j in indexes_to_del:
            del query_words[j]

        return query_words

    def initialize_dic(self):
        if self.run_with_stemming:
            directory = "part2 with stemming"
        else:
            directory = "part2"
        is_title = True

        # Initialize stop words array
        try:
            stop_words_csv = open(directory + "/movies_stop_words.csv")
            stop_words_reader = UnicodeReader(stop_words_csv)
            for line in stop_words_reader:
                if is_title:
                    is_title = False
                    continue
                self.movies_stop_words[line[0]] = "0"
            stop_words_csv.close()
        except Exception as e:
            print "Something went wrong with stop words file " + str(e.message)

        # Initialize idf dic
        try:
            is_title = True
            idf_csv = open(directory + "/idf.csv")
            idf_reader = UnicodeReader(idf_csv)
            for line in idf_reader:
                if is_title:
                    is_title = False
                    continue
                self.idf_dic[line[0]] = line[1]
            idf_csv.close()
        except Exception as e:
            print "Something went wrong with idf file " + str(e.message)

        # Initialize terms in doc
        try:
            is_title = True
            terms_csv = open(directory + "/terms_in_document.csv")
            terms_reader = UnicodeReader(terms_csv)
            for line in terms_reader:
                if is_title:
                    is_title = False
                    continue
                self.terms_in_document[line[0]] = line[1]
            terms_csv.close()
        except Exception as e:
            print "Something went wrong with terms in doc file " + str(e.message)

        # Initialize tf dic
        try:
            is_title = True
            tf_csv = open(directory + "/tf.csv")
            tf_reader = UnicodeReader(tf_csv)
            for line in tf_reader:
                if is_title:
                    is_title = False
                    continue
                word = line[0]
                term_tf = {}
                for i in range(1, len(line) - 1, 2):
                    term_tf[line[i]] = line[i + 1]
                self.tf_dic[word] = term_tf
            tf_csv.close()
        except Exception as e:
            print "Something went wrong with tf file " + str(e.message)

    def create_movies_name_dic(self):
        movie_serial_num = 0
        movie_name = 2
        movie_link = 1
        is_title = True
        try:
            movies_csv = open("movies.csv", "r")
            movies_csv_reader = UnicodeReader(movies_csv)
            for line in movies_csv_reader:
                if is_title:
                    is_title = False
                    continue
                self.movies_name_dic[line[movie_serial_num]] = line[movie_name]
                self.movies_link_dic[line[movie_serial_num]] = line[movie_link]
        except Exception as e:
            print "Something went wrong with tf movies name dic " + str(e.message)




