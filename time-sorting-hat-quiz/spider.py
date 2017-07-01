import scrapy
from selenium import webdriver
import selenium.webdriver.chrome.service as service

class TimePotterQuizSpider(scrapy.Spider):
    name = 'timepotterquizspider'
    start_urls = ['http://time.com/4809884/harry-potter-house-sorting-hat-quiz/']

    def __init__(self):
        import os
        currdir = os.path.dirname(os.path.realpath(__file__))
        chromedriver_path = os.path.join(currdir,'../bin/chromedriver')
        os.environ["webdriver.chrome.driver"] = chromedriver_path
        self.driver = webdriver.Chrome(chromedriver_path)
        
    def parse(self, response):
        # div#harry_potter_house
        self.driver.get(self.start_urls[0])


        self.driver.close()
