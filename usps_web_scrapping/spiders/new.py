from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    # browser = p.chromium.launch(slow_mo = 50)
    browser = p.chromium.launch(headless=False, slow_mo = 50)
    page = browser.new_page()
    # page.goto('https://gateway.usps.com/eAdmin/view/signin')
    # page.click('input#login')
    
    # 
    page.goto('https://reg.usps.com/entreg/LoginBCGAction_input?app=EadminAPP&appURL=https://gateway.usps.com/eAdmin/view/signin/loginCheck')
    page.fill('input#username', 'aci.usps.devteam')
    page.fill('input#password', 'MFH1bmq6cea!bzv?ruk')
    # page.wait_for_selector('button#btn-submit')    
    page.click('button#btn-submit')    
    # page.click('button#btn-submit')
    

    # wait for 5 seconds
    time.sleep(5)
    page.click("a[title='Link to eVS']")
    time.sleep(5)
        
    # page.click('a[href="/PrsWeb/evs/ImpbNonComplianceDownload.do"]')
    # page.click('//a[contains(text(), "Download")]')
    # page.click("a[title='Having trouble accessing this report online? Try this feature to generate downloadable data files based on criteria you choose.']")
    # page.click('a:contains("[Download]")')
    # page.click("text=Download")
    # page.click('a[href="/PrsWeb/evs/ImpbNonComplianceDownload.do"]')
    # download_link = page.query_selector('a[content="[Download]"]')
    # download_link.click()
    page.goto('https://www.uspspostalone.com/PrsWeb/evs/ImpbNonComplianceDownload.do')
    # page.locator('a').get_by_text('Download').click()
    
    # download the files~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    import shutil

    with page.expect_download() as download_info:
        page.get_by_text("902478799_70929_1.csv").click()
    download = download_info.value

    # get the path of the downloaded file
    download_path = download.path()

    # move the downloaded file to a new location
    shutil.move(download_path, "902478799_70929_1.csv")

    