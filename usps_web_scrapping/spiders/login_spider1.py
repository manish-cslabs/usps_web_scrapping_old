import scrapy
import json
import requests
from utils import save_content_in_file


login_url = 'https://gateway.usps.com/eAdmin/view/signin'
login_cred = {
    'username': 'aci.usps.devteam',
    'password': 'MFH1bmq6cea!bzv?ruk'
}
csv_files_page_url= 'https://www.uspspostalone.com/PrsWeb/evs/ImpbNonComplianceDownload.do'
base_url = "https://www.uspspostalone.com/"

class LoginSpider(scrapy.Spider):
    name = 'login_spider1'
    # start_urls = [login_url]
    # start_urls = ['https://reg.usps.com/entreg/LoginBCGAction_input?app=EadminAPP&appURL=https://gateway.usps.com/eAdmin/view/signin/loginCheck']
    start_urls = ['https://reg.usps.com/entreg/LoginBCGAction_input']

    # parse
    def parse(self, response):
        save_content_in_file(response.text, "login.html")
        
        return scrapy.FormRequest.from_response(response,
                                                formdata=login_cred,
                                                callback=self.after_login)

    # after_login
    def after_login(self, response):
        save_content_in_file(response.text, "after_login.html")

        # Check if login was successful
        if "service" in response.text:
            # Login successful, start scraping the target page
            yield scrapy.Request(
                url=
                csv_files_page_url,
                callback=self.parse_target_page)
        else:
            # Login failed, handle the error
            self.logger.error("Login failed")

    # parse_target_page
    def parse_target_page(self, response):
        save_content_in_file(response.text, "parse_target_page.html")

        # Extract the URLs of the CSV files
        csv_links = response.xpath(
            '//a[contains(text(), ".csv")]/@href').getall()
        # # Download each CSV file
        for csv_link in csv_links:
            base_url = base_url
            csv_link = base_url + csv_link
            print("csv_link:", csv_link)
            # yield scrapy.Request(url=response.urljoin(csv_link),
            #                      callback=self.save_csv)

    # save_csv
    def save_csv(self, response):
        # Save the CSV file to disk
        filename = response.url.split("/")[-1]
        # save_content_in_file(response.body, filename)

        with open(filename, 'wb') as f:
            f.write(response.body)
