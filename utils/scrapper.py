# IMPORT NECCESSARY LIB
import os
import time
from utils.formatter import format_description_text
from utils.tweet import tweet



trigger_Words = ['Trailer', 'Chat', 'Reveal', 'Announcement', 'Overview', 'Teaser', 'Adventure', 'Year', 'Update', 'Hearthstone']
c_path = os.getcwd()

def scrape_youtube(driver, WebDriverWait, By, EC):
    driver.implicitly_wait(10)
    driver.get('https://www.youtube.com/c/Hearthstone/videos')

    videos = WebDriverWait(driver, 30).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "a.yt-simple-endpoint.style-scope.ytd-grid-video-renderer")))
    time.sleep(0.5)

    latest_video = None

    for video in videos: 
        print(video.text)
        tweeted = False
        if latest_video != None:
            break
        with open(c_path +"/data/data.txt") as f:
            for line in f:
                if line.strip() == video.get_attribute('href'):
                    tweeted = True
                    
        if tweeted:
            continue
        title = video.text
        print(title)
        for word in trigger_Words:
            if word.lower() in title.lower():
                with open(c_path +"/data/data.txt", "a") as file:
                    file.write(video.get_attribute('href') + '\n')
                latest_video = video.get_attribute('href')
                print(word)
                break

    if latest_video == None:
        return print('No Latest video......')
    else:
        driver.get(latest_video)
        
        time.sleep(10)

        intro = '📢 New Video Spotted 📢'
        try:
            description = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div#content div#description div.ytd-video-secondary-info-renderer yt-formatted-string.ytd-video-secondary-info-renderer span.yt-formatted-string"))).text
        except:
            description = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "yt-formatted-string.ytd-video-secondary-info-renderer > span.yt-formatted-string"))).text 
            # description = 'No Description'   

        url = driver.current_url
        print(description)
        desc = format_description_text(description)

        text = f"{intro}\n\n📺{title}\n\n\"{desc}\"\n\nSource: {url}"

        print('Youtube age...........................#####################################################')
        print(text)

        # UPLOAD TO TWITTER
        tweet(text)
        
        time.sleep(5)
        driver.quit()

