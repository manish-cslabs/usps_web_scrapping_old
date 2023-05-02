import scrapy
from utils import save_content_in_file

class LoginSpider2(scrapy.Spider):
    name = 'login_spider2'
    start_urls = ['https://gateway.usps.com/eAdmin/view/signin']


    def parse(self, response):
        save_content_in_file(response.text, "before_login1.html")
        # Find and click the login button
        login_button = response.xpath("//input[@value='Sign in to the BCG']")
        yield scrapy.FormRequest.from_response(
            response,
            formdata=None,
            clickdata={'type': 'button', 'id': login_button.xpath('./@id').get()},
            callback=self.login
        )

    def login(self, response):
        save_content_in_file(response.text, "login.html")
        
        # Submit the login form with username and password
        yield scrapy.FormRequest.from_response(
            response,
            formdata={'username': 'your_username', 'password': 'your_password'},
            callback=self.after_login
        )

    def after_login(self, response):
        save_content_in_file(response.text, "after_login.html")
        
        # Check if login was successful
        if "Welcome" in response.text:
            # Login successful, start scraping the target page
            yield scrapy.Request(url='https://example.com/target_page', callback=self.parse_target_page)
        else:
            # Login failed, handle the error
            self.logger.error("Login failed")

    def parse_target_page(self, response):
        # Scrape the target page
        pass










