import json, time
from parsel import Selector
from utils.utils import write_url

def get_page_source(driver, url):
	driver.get(url)
	
	old_height = driver.execute_script("""
		function getHeight() {
			return document.querySelector('ytd-app').scrollHeight;
		}
		return getHeight();
	""")
	
	while True:
		driver.execute_script("window.scrollTo(0, document.querySelector('ytd-app').scrollHeight)")
	
		time.sleep(1.5)
	
		new_height = driver.execute_script("""
			function getHeight() {
				return document.querySelector('ytd-app').scrollHeight;
			}
			return getHeight();
		""")
	
		if new_height == old_height:
			break
	
		old_height = new_height
	
	selector = Selector(driver.page_source)
	# driver.quit()
	
	return selector

def scrape_video_data(selector, url):
	video_data = []
	
	title = selector.css(".title .ytd-video-primary-info-renderer::text").get()
	description = selector.css(".ytd-expandable-video-description-body-renderer span:nth-child(1)::text").get()

	video_data.append({
		"title": title,
		"description": description,
		"url": url
	})

	write_url(url)
	
	print(json.dumps(video_data, indent=2, ensure_ascii=False))
	return video_data


