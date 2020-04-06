import scrapy
from scrapy import Selector
from urllib.parse import urlparse
from bs4 import BeautifulSoup
#import mysql.connector

class My_spider(scrapy.Spider):
    name = "MySpider"

    start_urls = [
        "https://fr.m.wikipedia.org/wiki/Web_scraping"
    ]

    def parse(self, response):

        parsed_url = urlparse(response.url)
        print("Domain Currenttly being crawled is : {url.scheme}://{url.netloc} \n".format(url=parsed_url))
        PRINT("HEADERS USED NOW ARE : " + response.request.headers)


        title = Selector(response).css('title ::text').get()
        soup = BeautifulSoup(response.text, features='lxml')
        code_source = soup
        for script in soup(["script", "style","nav"]):
            script.extract()

        contents = soup.get_text()
        #print(contents + '\n\n\n')
        lines = (line.strip() for line in contents.splitlines())
        contents = '\n'.join(line for line in lines if line)

        domain = response.url
        #print(title + '\n\n\n')
        #print(contents + '\n\n\n')
        #print("Tha Domain is " + domain)
        links = response.css('a')
        yield from response.follow_all(links, callback = self.parse)

    def insert_data(title, contents, url, code_source):
        try:
            req = """INSERT IGNORE INTO websites (title, contents, url, code_source)
                        VALUES ('{}', '{}', '{}', '{}');""".format(title, contents, url, code_source)
            cursor.execute(req)

        except (KeyError, IndexError, TypeError) as error:
            print("There was an error during articles insertion. The error: {}".format(error))




    def random_headers():

        accepts = {"Firefox": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Safari, Chrome": "application/xml,application/xhtml+xml,text/html;q=0.9, text/plain;q=0.8,image/png,*/*;q=0.5"}

        try:
            user_agent = UserAgent()
            if random.random() > 0.5:
                chosen_user_agent = user_agent.Chrome
            else:
                chosen_user_agent = user_agent.Firefox

        except FakeUserAgentError as error:
            print("the chosen FakeUserAgent didn't work; the error is {}".format(error))
            user_agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
                        "Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1"]  # Just for case user agents are not extracted from fake-useragent package
            chosen_user_agent = random.choice(user_agents)

        finally:
            valid_accept = accepts['Firefox'] if chosen_user_agent.find('Firefox') > 0 else accepts['Safari, Chrome']
            headers = {"User-Agent": chosen_user_agent, "Accept": valid_accept}

        return headers









    '''def build_database(db_name, host_name, user_name, password, sqltable):

        my_db = mysql.connector.connect(host=host_name, user=user_name, passwd=password, database=db_name)
        cursor = my_db.cursor()
        cusror.execute(sqltable)
        my_db.commit()
        print("\n*** Database was created successfully. ***\n")

        except mysql.connector.Error as error:
            my_db.rollback()  # rollback if any exception occured
            print("Failed creating database {}.".format(error))

        finally:
            if my_db is not None and my_db.is_connected():
            cursor.close() ; my_db.close()
            logger.info("MySQL connection is closed.")
        else:
            print("connection to MySQL did not succeed.")


    #all_sql_tables = [...]

    # An example of a single table creation called "articles" in SQL command
    sql_website_table = """CREATE TABLE IF NOT EXISTS websites (ID int AUTO_INCREMENT,
                                                     title varchar(255),
                                                     contents TEXT,
                                                     url varchar(255),
                                                     PRIMARY KEY(ID));"""
    #all_sql_tables.append(sql_articles) # list of all sql tables creation


        def _clean(value):
            value = ' '.join(value)
            value = value.replace('\n', '')
            value = unicodedata.normalize("NFKD", value)
            value = re.sub(r' , ', ', ', value)
            value = re.sub(r' \( ', ' (', value)
            value = re.sub(r' \) ', ') ', value)
            value = re.sub(r' \)', ') ', value)
            value = re.sub(r'\[\d.*\]', ' ', value)
            value = re.sub(r' +', ' ', value)
            return value.strip() '''
