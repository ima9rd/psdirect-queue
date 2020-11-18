from selenium import webdriver, common
from webdriver_manager.chrome import ChromeDriverManager
from random import randint
import time
import pyttsx3

CAPTCHA_TIME_ALLOWANCE = 30

speakengine = pyttsx3.init()

def say(message, repeat=1):
    for i in range(repeat):
        speakengine.say(message)
        speakengine.runAndWait()

def schedule_refresh():
    time.sleep(randint(4, 10))
    sel.refresh()
    print('refreshing')

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
        say("ps5 queue is active")
    elif body.get_attribute('class') == 'softblock':
        say("captcha-challenge block")
        time.sleep(CAPTCHA_TIME_ALLOWANCE) # allow 20 seconds to solve captcha before attempting to refresh
    else:
        schedule_refresh()
