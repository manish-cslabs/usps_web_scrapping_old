import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest

class BCGSpider(scrapy.Spider):
    name = 'bcg_spider'
    start_urls = ['https://gateway.usps.com/eAdmin/view/signin'] # change this to your desired start URL
    
    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse)
    
    def parse(self, response):
        filename = "before_login1.html"
        with open(filename, 'w') as f:
            f.write(response.text)
            
        # Click the "Sign in to the BCG" button
        btn = response.meta['driver'].find_element_by_xpath('//input[@id="login"]')
        btn.click()
        
        # Yield the next page
        yield SeleniumRequest(url=response.url, callback=self.login)
        
    def login(self, response):
        filename = "login.html"
        with open(filename, 'w') as f:
            f.write(response.text)
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
    
    def parse_target_page(self, response):
        filename = "after_login.html"
        with open(filename, 'w') as f:
            f.write(response.text)
        # Extract the URLs of the CSV files and download them
        csv_links = response.css('a[href$=".csv"]::attr(href)').getall()
        for csv_link in csv_links:
            yield {'file_urls': [csv_link]}
