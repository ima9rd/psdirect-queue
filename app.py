from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import time
import pyttsx3
import zipfile
import glob
import os


PROXY_LIST = [{'ip_address': '', 'port': '', 'username': '', 'password': ''}]
PAUSE_DURATION = 5
CAPTCHA_PAUSE_DURATION = 30

speakengine = pyttsx3.init()

def say(message: str, repeat: int=1) -> None:
    for i in range(repeat):
        speakengine.say(message)
        speakengine.runAndWait()

def spawn_browser(proxy_dict: dict, index: int) -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    if len(proxy_dict['ip_address']) > 0:
        plugin_file = create_proxy_extension(proxy_dict, index)
        options.add_extension(plugin_file)
    return webdriver.Chrome(ChromeDriverManager().install(), options=options)

def create_proxy_extension(proxy_dict: dict, index: int) -> str:
    manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """
    background_js = f"""
        var config = {{
                mode: "fixed_servers",
                rules: {{
                singleProxy: {{
                    scheme: "http",
                    host: "{proxy_dict['ip_address']}",
                    port: parseInt({proxy_dict['port']})
                }},
                bypassList: ["localhost"]
                }}
            }};

        chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});

        function callbackFn(details) {{
            return {{
                authCredentials: {{
                    username: "{proxy_dict['username']}",
                    password: "{proxy_dict['password']}"
                }}
            }};
        }}

        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {{urls: ["<all_urls>"]}},
                    ['blocking']
        );
        """
    plugin_file = f'proxy_auth_plugin_{index}.zip'
    with zipfile.ZipFile(plugin_file, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)
    return plugin_file

def close_losers(winner: webdriver.Chrome, browsers: list) -> None:
    for browser in browsers:
        if browser != winner:
            browser.close()

def clean_up_extensions() -> None:
    for f in glob.glob('proxy_auth_plugin_*.zip'):
        os.remove(f)

browsers = list()
for i, prox in enumerate(PROXY_LIST):
    browsers.append(spawn_browser(prox, i))
queue = False
captcha = False
while not queue:
    for sel in browsers:
        if queue:
            pass
        else:
            try:
                if sel.current_url == 'data:,' or not captcha:
                    sel.get('https://direct.playstation.com/en-us/ps5')
                body = sel.find_element_by_tag_name('body')
                if body.get_attribute('class') == 'queue challenge':
                    queue = True
                    close_losers(sel, browsers)
                    clean_up_extensions()
                    sel.maximize_window()
                    say('ps5 queue is active')
                    input()
                elif body.get_attribute('class') == 'softblock':
                    say('captcha-challenge block')
                    if not captcha:
                        captcha = True
                        sel.maximize_window()                                      
                    time.sleep(CAPTCHA_PAUSE_DURATION)
                else:
                    captcha = False
                    time.sleep(PAUSE_DURATION)
            except WebDriverException:
                pass
                