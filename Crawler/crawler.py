# -*- coding: utf-8 -*-
import os
import urllib2
from BeautifulSoup import BeautifulSoup, NavigableString, Tag
from HTMLParser import HTMLParser
from EncoderUTF8 import UnicodeWriter, UnicodeReader

__author__ = 'Ilya and Tzuria'


# This class Crawlers a movie summary site
class Crawler:
    siteUrl = "http://www.torec.net"
    visited = []  # List for keeping the urls we visited
    visited_name_movie = []
    csv_counter = 1  # Counter for the movie file number
    urls_to_visit = ["http://www.torec.net/movies_subs.asp"]
    page_url = "http://www.torec.net/movies_subs.asp"
    page_number = 2
    directory = "movies/"
    part_two = "part2/"
    MAX_FILE_NUMBER = 5000

    # constructor that make a csv file tha saves all the meta data of each movie
    def __init__(self):
        self.csv_file = open('movies.csv', 'w')
        self.writer = UnicodeWriter(self.csv_file)
        fieldnames = ['מספר סידורי', 'קישור-באתר', 'שם הסרט', 'שנה', 'אורך', "ז'אנר", 'שחקנים', 'תיקייה']
        self.writer.writerow(fieldnames)
    # the main function that start the crawling

    # Method that makes all the crawler work
    def spider(self):
        while len(self.urls_to_visit) > 0:
            if self.page_number > 664:
                break
            if self.csv_counter > self.MAX_FILE_NUMBER:
                break
            crawl_url = self.urls_to_visit[0]
            if crawl_url not in self.visited:
                # Enter the movie and get the meta data
                if crawl_url.startswith('http://www.torec.net/movies_subs.asp'):
                    self.subs_page_spider(crawl_url)
                # Continue crawling and getting movies urls
                if crawl_url.startswith('http://www.torec.net/sub.asp'):
                    self.sub_page_spider(crawl_url)
            else:
                self.urls_to_visit.pop(0)

    # Spider a page for all its links
    def subs_page_spider(self, crawl_url):
        self.urls_to_visit.pop(0)
        try:
            page = urllib2.urlopen(crawl_url).read()
            self.visited.append(crawl_url)
        except Exception as e:
            self.urls_to_visit.append(crawl_url)
            print str(e.message)
            return
        soup = BeautifulSoup(page)
        for div in soup.findAll("div", {"class": "name"}):
            link = div.findChild('a')
            new_url = self.siteUrl + link.get('href')
            # Crawl the page if we didn't visit him before
            if new_url not in self.urls_to_visit and new_url not in self.visited:
                self.urls_to_visit.append(new_url)
        # Continue the crawl on the pages by increase the page number
        new_page = self.page_url + "?p=" + str(self.page_number)
        self.urls_to_visit.append(new_page)
        self.page_number += 1

    # Crawl the page and get all the movie data
    def sub_page_spider(self, crawl_url):
        self.urls_to_visit.pop(0)
        try:
            page = urllib2.urlopen(crawl_url).read()
            self.visited.append(crawl_url)
        except Exception as e:
            print str(e.message)
            self.urls_to_visit.append(crawl_url)
            return
        soup = BeautifulSoup(page)
        html_parser = HTMLParser()
        year = genre = length = " "
        actors = []
        movie_title = soup.find("div", {"class": "line sub_title"}).findChild("h1").text.strip()
        movie_title = html_parser.unescape(movie_title)
        # Remove ":" from title if needed
        if movie_title.__contains__(':'):
            movie_title_temp = movie_title.split(":")
            movie_title = "".join(movie_title_temp)
        if movie_title in self.visited_name_movie:
            return
        self.visited_name_movie.append(movie_title)

        movie_summary = soup.find("div", {"class": "sub_name_div"}).text
        movie_summary = html_parser.unescape(movie_summary.strip('START INDEX'))
        element = soup.find("span", {"class": "sub_name_span"})
        # Lopping on the element to get all the meta data of the movie
        for index in range(0, len(element)):
            if isinstance(element.contents[index], Tag):
                if element.contents[index].text.encode("utf-8") == "שנה:":
                    year = html_parser.unescape(element.contents[index + 1].strip())
                if element.contents[index].text.encode("utf-8") == "אורך:":
                    length = html_parser.unescape(element.contents[index + 1].strip())
                if element.contents[index].text.encode("utf-8") == "ז'אנר:":
                    genre = html_parser.unescape(element.contents[index + 1].strip())
        for a in element.findChildren('a'):
            actors.append(html_parser.unescape(a.text))
        actors = " ".join(actors)
        self.create_file(movie_title, movie_summary.encode("utf-8"))
        # Attaching all the meta data to the csv file
        path = "movies/" + movie_title + ".txt"
        movie_details = []
        movie_details.extend([self.csv_counter, crawl_url.encode("utf-8"), movie_title.encode("utf-8"),
                              year.encode("utf-8"), length.encode("utf-8"), genre.encode("utf-8"),
                              actors.encode("utf-8"), path.encode("utf-8")])
        self.writer.writerow(movie_details)
        # Increase the movie counter
        self.csv_counter += 1
        print self.csv_counter

    # Method that create a file with the movie name and write the movie summary inside.
    # Prams: movie name for the file name and movie summary for the file data
    def create_file(self, movie_name, movie_summary):

        directory = "movies"
        if not os.path.exists(directory):
            os.makedirs(directory)
        try:
            movie_file = open(self.directory + movie_name + ".txt", 'w')  # Trying to create a new file or open one
            movie_file.write(movie_summary)
            movie_file.close()
        except Exception as e:
            print('Something went wrong with the movie summary! Can\'t tell what? ' + str(e.message))

    def __del__(self):
        self.csv_file.close()


emp1 = Crawler()
emp1.spider()


