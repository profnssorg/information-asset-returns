import os
import time

os.system('open -a Docker')

time.sleep(60)

os.system('docker pull scrapinghub/splash')

time.sleep(30)

os.system('docker run -it -p 8050:8050 scrapinghub/splash --max-timeout 6000')

time.sleep(15)

os.system('scrapy crawl g1 -o g1.json')
