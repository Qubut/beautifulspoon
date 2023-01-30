import imgs_scraper
import requests

result = imgs_scraper.findAllImgs(requests.get('https://riem-apotheke.de/index.html').text)

print(imgs_scraper.extractImgsUrls(result))
