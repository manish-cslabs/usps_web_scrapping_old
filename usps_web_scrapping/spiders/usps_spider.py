import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from utils import save_content_in_file



# USPSSpider
class USPSSpider(scrapy.Spider):
    name = 'usps_spider'
    start_urls = ['https://gateway.usps.com/eAdmin/view/signin'] 
    
    # start_requests
    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse)
    
    # parse
    def parse(self, response):
        filename = "before_login.html"
        save_content_in_file(response.text, filename)
        
        # Click the "Sign in to the BCG" button
        btn = response.meta['driver'].find_element_by_xpath('//input[@id="login"]')
        btn.click()
        
        # Yield the next page
        yield SeleniumRequest(url=response.url, callback=self.login)
        
    # login
    def login(self, response):
        filename = "login.html"
        save_content_in_file(response.text, filename)
        
        # Fill in the username and password fields
        sel = Selector(response)
        username = 'aci.usps.devteam'
        password = 'MFH1bmq6cea!bzv?ruk'
        sel = sel.xpath('//form[@id="loginForm"]')
        sel.xpath('.//input[@id="username"]').send_keys(username)
        sel.xpath('.//input[@id="password"]').send_keys(password)
        
        # Click the "Sign in" button
        btn = sel.xpath('.//button[@id="btn-submit"]')
        btn.click()
        
        # Yield the next page
        yield SeleniumRequest(url=response.url, callback=self.parse_target_page)
    
    
    # parse_target_page
    def parse_target_page(self, response):
        filename = "parse_target_page.html"
        save_content_in_file(response.text, filename)
        
        # Extract the URLs of the CSV files and download them
        csv_links = response.css('a[href$=".csv"]::attr(href)').getall()
        for csv_link in csv_links:
            yield {'file_urls': [csv_link]}
