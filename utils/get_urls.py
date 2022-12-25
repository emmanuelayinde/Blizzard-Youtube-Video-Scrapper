from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from utils.utils import check_if_tweeted


def get_urls(driver, WebDriverWait, By, EC):
    driver.get('https://www.youtube.com/c/Hearthstone/videos')
    ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)

    wait = WebDriverWait(driver, 20, ignored_exceptions=ignored_exceptions)
    videos = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//div[@id="contents" and @class="style-scope ytd-rich-grid-renderer"]/ytd-rich-grid-row/div/ytd-rich-item-renderer/div/ytd-rich-grid-media')))[:5]
   
    print("Video..................", len(videos))

    videos_url = []

    for video in videos: 
        a = video.find_element(By.XPATH, './/div/div[2]/div/h3/a').get_attribute('href')
        if check_if_tweeted(a):
            continue
        else:
            videos_url.append(a)

    # driver.quit()
    print("Video Urls..........", videos_url)
    return videos_url
   



