#Importing main libraries
import scrapy
from scrapy import Selector
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import mysql.connector
from ..items import MyspiderItem


#implemeanting our spider class
class My_spider(scrapy.Spider):
    name = "Myspider"

    #here we present the urls to our spider to begin with, these are given to parse function to be dealt with
    start_urls = [
        #"https://fr.m.wikipedia.org/wiki/Web_scraping",
        'https://www.wikihow.com/Category:Sports-and-Fitness'
    ]

    #sql_table = """CREATE TABLE IF NOT EXISTS websites (ID int AUTO_INCREMENT,
    #                                                 title varchar(255),
    #                                                 contents TEXT,
    #                                                 url varchar(255),
    #                                                 code_source TEXT,
    #                                                 PRIMARY KEY(ID));"""

    #This is the main function that
    def parse(self, response):

        parsed_url = urlparse(response.url)
        #Some infos on the domain crawled and the headers used in the process
        print("Domain Currenttly being crawled is : {url.scheme}://{url.netloc} \n".format(url=parsed_url))
        print("HEADERS USED NOW ARE : " + str(response.request.headers))

        #We select the inforamtions nedeed to be extracted
        title = Selector(response).css('title ::text').get()
        soup = BeautifulSoup(response.text, features='lxml')
        code_source = soup
        # We get rid of the uncecessary tags from the code parsed
        for script in soup(["script", "style","nav", "form","address", "audio", "video"]):
            script.extract()

        #We extract the full text from website
        contents = soup.get_text()
        #print(contents + '\n\n\n')
        lines = (line.strip() for line in contents.splitlines())
        contents = '\n'.join(line for line in lines if line)

        print(title + '\n\n\n')
        #print(contents + '\n\n\n')
        #print("Tha Domain is " + domain)

        #Storing our data extracted
        items = MyspiderItem()
        items['title'] = title
        items['url'] = response.url
        items['contents'] = contents
        #We let our framework to pass the fiven information to the responsable pipeline
        yield items

        #We extracted all the links of the webpage and start crawling them
        links = response.css('a')
        #print(links)
        yield from response.follow_all(links, callback = self.parse)
