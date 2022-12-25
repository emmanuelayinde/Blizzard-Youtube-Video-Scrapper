# IMPORT NECCESSARY LIB
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
from utils.date import now
from utils.utils import Tweet
from utils.get_urls import get_urls
from utils.video_data import get_page_source, scrape_video_data

# CONFIG FOR PRODUCTION ENV
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service=Service(chromedriver_autoinstaller.install()), options=chrome_options)         



def main():
    print('Scraping Youtube...........................', now())

    urls = get_urls(driver, WebDriverWait, By, EC)

    data = []

    for url in urls:
        sc = get_page_source(driver, url)
        time.sleep(2)
        d = scrape_video_data(sc, url)
        data.append(d[0])
    
    driver.quit()
   
    if len(data):
        for d in data:
            Tweet(d)
    else:
        print("No latest video")


if __name__ == "__main__":
    main()
