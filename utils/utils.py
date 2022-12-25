import os
from operator import itemgetter
from utils.tweet import tweet
from utils.formatter import format_description_text

trigger_Words = ['Trailer', 'Chat', 'Reveal', 'Announcement', 'Overview', 'Teaser', 'Adventure', 'Year', 'Update', 'Hearthstone']
c_path = os.getcwd()

def check_if_tweeted(id):
    with open(c_path + "/data/data.txt") as f:
        if id in f.read():
            return True
    return False


def write_url(url):
    with open(c_path + "/data/data.txt", "a") as file:
        file.write(url + '\n')
    return True


def check_keyword(t): 
    for word in trigger_Words:
        if word.lower() in t.lower():
            print(word, t)
            return True
    print(t)
    return False


def Tweet(data):
    title, description, url = itemgetter('title', 'description', 'url')(data)
    print(title, description, url)

    intro = '📢 New video spotted 📢'

    print(description)

    t = f"{intro}\n\n📺 {title}\n\n📺 \n\n🌐 {url}\n\n{url}"
    desc = format_description_text(description, len(t))

    text = f"{intro}\n\n📺 {title}\n\n📺 {desc}\n\n🌐 {url}\n\n{url}"

    print(text)

    # Tweet to twitter
    # tweet(text)   
    