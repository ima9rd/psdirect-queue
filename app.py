from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from random import randint
import time

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
sel = webdriver.Chrome(ChromeDriverManager().install(), options=options)
sel.delete_all_cookies()
sel.get('https://direct.playstation.com/en-us/ps5')

queue = False
while not queue:
    body = sel.find_element_by_tag_name('body')
    if body.get_attribute('class') == 'queue challenge':
        queue = True
    else:
        time.sleep(randint(4, 10))
        sel.refresh()
