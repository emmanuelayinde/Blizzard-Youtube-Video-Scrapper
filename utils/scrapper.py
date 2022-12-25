# IMPORT NECCESSARY LIB
import os
import time
from utils.date import now
from utils.formatter import format_description_text
from utils.tweet import tweet
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException



trigger_Words = ['Trailer', 'Chat', 'Reveal', 'Announcement', 'Overview', 'Teaser', 'Adventure', 'Year', 'Update', 'Hearthstone']
c_path = os.getcwd()

def scrape_youtube(driver, WebDriverWait, By, EC):
    driver.get('https://www.youtube.com/c/Hearthstone/videos')
    ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)

    wait = WebDriverWait(driver, 20, ignored_exceptions=ignored_exceptions)

    # videos = wait.until(EC.visibility_of_all_elements_located((By.XPATH, "a.yt-simple-endpoint.style-scope.ytd-grid-video-renderer")))
    # //div[@id="contents" and @class="style-scope ytd-rich-grid-renderer"]/ytd-rich-grid-row/div/ytd-rich-item-renderer/div/ytd-rich-grid-media/div/ytd-thumbnail
    videos = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//div[@id="contents" and @class="style-scope ytd-rich-grid-renderer"]/ytd-rich-grid-row/div/ytd-rich-item-renderer/div/ytd-rich-grid-media')))[:5]
    
    print("Video..................", len(videos))
    time.sleep(2)

    latest_video = None
    t = None
    a = None

    n = 0
    for video in videos: 
        t = video.find_element(By.XPATH, './/div/div[2]/div/h3').text
        a = video.find_element(By.XPATH, './/div/div[2]/div/h3/a').get_attribute('href')
        print(n, t)
        print(n, a)
        n += 1

        tweeted = False
        tweetable = False

        with open(c_path +"/data/data.txt") as f:
            if a in f.read():
                tweeted = True

        if tweeted:
            continue

        d = get_description(driver, WebDriverWait, By, EC, a)

        for word in trigger_Words:
            if word.lower() in t.lower():
                with open(c_path +"/data/data.txt", "a") as file:
                    file.write(a + '\n')
                latest_video = a
                tweetable = True
                print(word, t, a)
                break


        if tweetable:
            break
        else:
            continue

    if latest_video == None:
        return print('No Latest video......', now())
    else:
        intro = '📢 New video spotted 📢'

        # print(description)
        # desc = format_description_text(description)
        text = f"{intro}\n\n📺 {t}\n\n🌐 {a}\n\n{a}"
        # text = f"{intro}\n\n📺 {t}\n\n{a}"

        print(text)

        # UPLOAD TO TWITTER
        # tweet(text)   
        
        driver.quit()



def get_description(driver, WebDriverWait, By, EC, link):
    driver.get(link)
    wait = WebDriverWait(driver, 20)

    try:
        description = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//ytd-text-inline-expander[@id="description-inline-expander" and @class="style-scope ytd-watch-metadata"]/yt-formatted-string[@class="style-scope ytd-text-inline-expander"]/span[@class="style-scope yt-formatted-string"]')))[0].text
    except:
        # description = wait.until(EC.visibility_of_element_located((By.XPATH, "yt-formatted-string.ytd-video-secondary-info-renderer > span.yt-formatted-string"))).text 
        description = 'No Description'   

    print("Description", description)
    return description