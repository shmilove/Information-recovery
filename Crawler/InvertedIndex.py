# -*- coding: utf-8 -*-
import os

import math

from EncoderUTF8 import UnicodeReader, UnicodeWriter
from runTagger import call_meni

__author__ = 'Ilya and Tzuria'
run_with_stemming = True
metadata_weight = 2


class InvertedIndex:
    def __init__(self):
        self.total_number_of_documents = 0
        pass

    inverted_index_dic = {}
    movies_frequency_words = {}
    movies_stop_words = []
    terms_in_document = {}
    need_metadata = True

    def create_inverted_index(self):
        movie_serial_num = 0
        movie_path = 7
        movie_name = 2
        movie_year = 3
        movie_actors = 6
        is_title = True
        try:
            csv_file = open('movies.csv', 'r')
            reader = UnicodeReader(csv_file)
            for line in reader:
                if is_title:
                    is_title = False
                    continue
                # if int(line[movie_serial_num]) > 300:
                #     break
                self.add_to_inverted_index_dic(line[movie_serial_num], line[movie_path])
                if self.need_metadata:
                    self.add_metadata_to_index_dic(line[movie_serial_num], line[movie_name], line[movie_year],
                                               line[movie_actors])
                self.need_metadata = True

            csv_file.close()

        except Exception as e:
            print("Something went wrong with inverted index: " + str(e.message))

        # Create word frequency file according to the inverted index
        self.create_movies_frequency_words()

        # Create a stop word file according to a certain words that repeat themselves above 5% of the total words
        #  in the index
        self.create_movies_stop_words_file()

        # Create the inverted index without the stop words in it
        self.create_inverted_index_file()

        self.create_tf_idf_file()

        self.create_terms_in_document_file()

    # Add meta data to the inverted index dic
    def add_metadata_to_index_dic(self, serial_num, name, year, actors):
        # Add movie name
        name = name.replace(",", " ").replace('(', '').replace(')', '').replace('.', ' ')\
                .replace('"', ' ').replace('!', ' ').replace('?', ' ').replace("'", '')
        actors = actors.replace(",", " ").replace('(', '').replace(')', '').replace('.', ' ')\
                .replace('"', ' ').replace('!', ' ').replace('?', ' ').replace("'", '')
        if run_with_stemming:
            name = call_meni(name.encode("utf-8"))
            actors = call_meni(actors.encode("utf-8"))
        name_arr = name.split()
        try:
            for word in name_arr:
                word = word.encode("utf-8")
                if word in self.inverted_index_dic.keys():
                    word_arr = self.inverted_index_dic.get(word)
                    if serial_num in word_arr.keys():
                        word_arr[serial_num] += metadata_weight
                    else:
                        word_arr[serial_num] = metadata_weight
                else:
                    value = {serial_num: metadata_weight}
                    self.inverted_index_dic[word] = value
                self.terms_in_document[serial_num.encode("utf-8")] += metadata_weight
        except Exception as e:
            print "Something went wrong with add movie name in metadata " + str(e.message)
        # Add year
        if year is not "":
            year = year.encode("utf-8")
            if year in self.inverted_index_dic.keys():
                word_arr = self.inverted_index_dic.get(year)
                if serial_num in word_arr.keys():
                    word_arr[serial_num] += metadata_weight
                else:
                    word_arr[serial_num] = metadata_weight
            else:
                value = {serial_num: metadata_weight}
                self.inverted_index_dic[year] = value
            self.terms_in_document[serial_num.encode("utf-8")] += metadata_weight
        # Add actors
        actors_arr = actors.split()
        for actor in actors_arr:
            actor = actor.encode("utf-8")
            if actor in self.inverted_index_dic.keys():
                word_arr = self.inverted_index_dic.get(actor)
                if serial_num in word_arr.keys():
                    word_arr[serial_num] += metadata_weight
                else:
                    word_arr[serial_num] = metadata_weight
            else:
                value = {serial_num: metadata_weight}
                self.inverted_index_dic[actor] = value
            self.terms_in_document[serial_num.encode("utf-8")] += metadata_weight

    # Create the movie stop words file from the inverted index dictionary
    def create_movies_stop_words_file(self):
        file_name = "movies_stop_words.csv"
        if run_with_stemming:
            directory = "part2 with stemming"
        else:
            directory = "part2"

        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
            movies_stop_words_csv = open(directory + "/" + file_name, "w+")
            stop_words_writer = UnicodeWriter(movies_stop_words_csv)
            fieldnames = ['מילה']
            stop_words_writer.writerow(fieldnames)
            movie_index_size = len(self.inverted_index_dic.keys())
            stop_word_flag = movie_index_size * 0.02

            for word in self.movies_frequency_words.keys():
                word_dic = self.movies_frequency_words[word]
                if word_dic >= stop_word_flag:
                    self.movies_stop_words.append(word)

            for word in self.movies_stop_words:
                if word in self.inverted_index_dic.keys():
                    del self.inverted_index_dic[word]
                stop_words_writer.writerow([word, self.movies_frequency_words[word]])
            movies_stop_words_csv.close()
        except Exception as e:
            print("Something went wrong with stop words file: " + str(e.message))

    # Create the inverted index file from the inverted index dictionary
    def create_inverted_index_file(self):
        inverted_file_name = "inverted_index.csv"
        if run_with_stemming:
            directory = "part2 with stemming"
        else:
            directory = "part2"
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)

            inverted_index_file = open(directory + "/" + inverted_file_name, "w+")
            inverted_index_writer = UnicodeWriter(inverted_index_file)
            fieldnames = ['מילה', 'מספר מופעים<- מספר סידורי']
            inverted_index_writer.writerow(fieldnames)
            for word in self.inverted_index_dic.keys():
                word_dic = self.inverted_index_dic[word]
                words_index = []
                for serial_num in word_dic.keys():
                    pair = serial_num + "->" + str(word_dic[serial_num])
                    words_index.append(pair)
                temp_words_index = [word]
                temp_words_index.extend(words_index)
                inverted_index_writer.writerow(temp_words_index)
            inverted_index_file.close()
        except Exception as e:
            print("Something went wrong with inverted index file: " + str(e.message))

    def add_to_inverted_index_dic(self, serial_num, movie_path):

        try:
            movie_file = open(movie_path, 'r')
            movie_summary = movie_file.read().decode("utf-8")
            movie_summary = movie_summary.replace(",", " ").replace('(', '').replace(')', '').replace('.', ' ')\
                .replace('"', ' ').replace('!', ' ').replace('?', ' ')
            if run_with_stemming:
                movie_summary = call_meni(movie_summary.encode("utf-8"))
            self.total_number_of_documents += 1
            description_arr = movie_summary.split()
            self.terms_in_document[serial_num] = len(description_arr)

            for word in description_arr:
                if word:
                    self.add_word_to_dictionary(serial_num, word)

        except Exception as e:
            self.need_metadata = False
            print "Something went wrong with the dictionary " + str(e.message)

    def add_word_to_dictionary(self, serial_num, word):

        if word.encode("utf-8") in self.inverted_index_dic.keys():
            word_arr = self.inverted_index_dic.get(word.encode("utf-8"))
            if serial_num in word_arr.keys():
                word_arr[serial_num] += 1
            else:
                word_arr[serial_num] = 1

        else:
            pairs = {serial_num.encode("utf-8"): 1}
            self.inverted_index_dic[word.encode("utf-8")] = pairs

    def create_movies_frequency_words(self):
        file_name = "movie_frequency.csv"
        if run_with_stemming:
            directory = "part2 with stemming"
        else:
            directory = "part2"

        for word in self.inverted_index_dic.keys():
            word_frequency = 0
            word_dic = self.inverted_index_dic[word]
            for serial_num in word_dic.keys():
                word_frequency += word_dic[serial_num]
                self.movies_frequency_words[word] = word_frequency
        try:
            movie_frequency_csv = open(directory + "/" + file_name, "w+")
            movie_frequency_writer = UnicodeWriter(movie_frequency_csv)
            fieldnames = ['מילה', 'מספר מופעים']
            movie_frequency_writer.writerow(fieldnames)
            for word in self.movies_frequency_words.keys():
                number = self.movies_frequency_words[word]
                movie_frequency_writer.writerow([word, number])
            movie_frequency_csv.close()
        except Exception as e:
            print "Something went wrong with stop words file " + str(e.message)

    def create_tf_idf_file(self):

        if run_with_stemming:
            directory = "part2 with stemming"
        else:
            directory = "part2"
        try:
            file_name = "idf.csv"
            idf_csv = open(directory + "/" + file_name, "w+")
            idf_writer = UnicodeWriter(idf_csv)
            fieldnames = ['מילה', 'idf']
            idf_writer.writerow(fieldnames)
            for word in self.inverted_index_dic.keys():
                # Number of documents with term t in it
                nodw = len(self.inverted_index_dic[word].keys())
                idf = math.log(self.total_number_of_documents / nodw)
                idf_writer.writerow([word, idf])
            idf_csv.close()
        except Exception as e:
            print "Something went wrong with idf file " + str(e.message)

        try:
            file_name = "tf.csv"
            tf_csv = open(directory + "/" + file_name, "w+")
            tf_writer = UnicodeWriter(tf_csv)
            fieldnames = ['מילה', 'מסמך', 'tf']
            tf_writer.writerow(fieldnames)
            counter = 0
            for word in self.inverted_index_dic.keys():
                counter += 1
                tf_arr = []
                temp_row = [word]
                for serial_num in self.inverted_index_dic[word].keys():
                    if serial_num == "3":
                        print "ssp"
                    number = int(self.inverted_index_dic[word][serial_num])
                    if serial_num in self.terms_in_document:
                        terms_in_document = self.terms_in_document[serial_num]
                        if terms_in_document > 0:
                            tf = float(number) / terms_in_document
                        else:
                            tf = 0
                    else:
                        tf = 0
                    tf_arr.append(serial_num)
                    tf_arr.append(str(tf))
                for value in tf_arr:
                    temp_row.append(value)
                tf_writer.writerow(temp_row)
            tf_csv.close()
        except Exception as e:
            print "Something went wrong with tf file " + str(e.message)

    def create_terms_in_document_file(self):
        file_name = "terms_in_document.csv"
        if run_with_stemming:
            directory = "part2 with stemming"
        else:
            directory = "part2"
        try:
            terms_csv = open(directory + "/" + file_name, "w+")
            terms_writer = UnicodeWriter(terms_csv)
            fieldnames = ['מסמך', 'גודל']
            terms_writer.writerow(fieldnames)
            for serial_num in self.terms_in_document.keys():
                terms_writer.writerow([serial_num, self.terms_in_document[serial_num]])
            terms_csv.close()
        except Exception as e:
            print "Something went wrong with create terms in doc file " + str(e.message)


inverted_index = InvertedIndex()
inverted_index.create_inverted_index()
