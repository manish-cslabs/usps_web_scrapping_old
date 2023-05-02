import scrapy
from selenium import webdriver

class northshoreSpider(scrapy.Spider):
    name = 'myspider'
    # allowed_domains = ['www.usps.com']    
    start_urls = ['https://gateway.usps.com/eAdmin/view/signin']


    def __init__(self):
        self.driver = webdriver.ChromiumEdge()

    def parse(self,response):
            self.driver.get('https://gateway.usps.com/eAdmin/view/signin')

            while True:
                try:
                    next = self.driver.find_element_by_xpath('//button[contains(text(), "Sign in to the BCG")]')
                    # login_button = response.xpath("//input[@value='Sign in to the BCG']")                    
                    url = 'https://gateway.usps.com/eAdmin/view/signin'
                    # yield scrapy.Request(url,callback=self.parse2)
                    next.click()
                except:
                    break

            self.driver.close()

    def parse2(self,response):
        print ('you are here!')


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# from selenium import webdriver

# # create a new Edge browser instance
# browser = webdriver.Edge()

# # navigate to the USPS eAdmin login page
# browser.get('https://gateway.usps.com/eAdmin/view/signin')

# # find the "Sign in to the BCG" button and click it

# button = browser.find_element_by_xpath('//button[contains(text(), "Sign in to the BCG")]')
# button.click()

