# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import errno
from mysql.connector import errorcode
import mysql.connector

class MyspiderPipeline(object):

    #config = {
    #    'user': 'root',
    #    'password': '',
    #    'host': '127.0.0.1',
    #    'port': '3308',
    #    'database': 'knowledge_data'
    #    }

#We start the connection to our databse
    def __init__(self, **kwargs):
        self.cnx = self.mysql_connect()

    def process_item(self, item, spider):
        return item

    def open_spider(self, spider):
        print("spider open")

    def process_item(self, item, spider):
        print("Saving item into db ...")
        self.save(item)
        return item

    def close_spider(self, spider):
        self.mysql_close()

    def mysql_connect(self):
        try:
            return mysql.connector.connect(user ='root', password= '', host = '127.0.0.1',port='3308', database='knowledge_data')

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

#this function store into our databse the parsed items
    def save(self, item):
        cursor = self.cnx.cursor()
        #Cheking if the value exists after rerunnig the spider
        exits_query = "SELECT * from websites where title = {} AND url = {} AND contents = {};".format(str(item['title']),str(item['url']),str(item['contents']))

        cursor.execute(exits_query)
        if cursor.rowcount==1:
            print("****** Value Already Exists *******")
            continue
        else:
            insert_query = """INSERT INTO websites (title, contents, url) VALUES (%s, %s, %s);"""

        # Insert new row
            cursor.execute(insert_query,(str(item['title']),str(item['contents']),str(item['url'])))

        # Make sure data is committed to the database
            self.cnx.commit()
        cursor.close()
        print("Items saved successfully")

    def mysql_close(self):
        self.cnx.close()
