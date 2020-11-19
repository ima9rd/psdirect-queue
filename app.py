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
    sel.delete_all_cookies()
    time.sleep(randint(4, 10))
    sel.refresh()

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
        say('ps5 queue is active')
        input()
    elif body.get_attribute('class') == 'softblock':
        say('captcha-challenge block')
        time.sleep(CAPTCHA_TIME_ALLOWANCE)
    else:
        try:
            button = sel.find_element_by_xpath('//button[@class="error-modal-popup__cta js-global-error-message-cta"]').click()
        except:
            pass
        schedule_refresh()
