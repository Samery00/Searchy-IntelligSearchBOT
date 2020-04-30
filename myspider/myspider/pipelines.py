# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import pymongo
from scrapy.exceptions import DropItem
import logging


class MyspiderPipeline(object):


# client = pymongo.MongoClient("mongodb+srv://root:<password>@cluster0-jbmri.mongodb.net/test?retryWrites=true&w=majority")
# db = client.test

    #configurations >> MongoDB
    MONGODB_SERVER = "localhost"
    MONGODB_PORT = 27017
    MONGODB_DB = "Knowledge_Base"
    MONGODB_COLLECTION = "websites"

#We start the connection to our databse
    def __init__(self):
        connection = pymongo.MongoClient("localhost", 27017)
        db = connection["Knowledge_Base"]
        self.collection = db["websites"]


#this function store into our databse the parsed items
    def process_item(self, item, spider):
        print("Saving item into db ...")
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
            logging.info("Item added to MongoDB database!",
                    level=logging.DEBUG, spider=spider)
        return item

    # def close_spider(self, spider):
    #     self.mysql_close()
