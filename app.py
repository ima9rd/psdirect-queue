from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import pyttsx3
import zipfile
import glob
import os


speakengine = pyttsx3.init()

def say(message, repeat=1):
    for i in range(repeat):
        speakengine.say(message)
        speakengine.runAndWait()

def spawn_proxy_browser(proxy_address: str, proxy_port:str, proxy_user: str, proxy_pass: str, index: int) -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
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
                    host: "{proxy_address}",
                    port: parseInt({proxy_port})
                }},
                bypassList: ["localhost"]
                }}
            }};

        chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});

        function callbackFn(details) {{
            return {{
                authCredentials: {{
                    username: "{proxy_user}",
                    password: "{proxy_pass}"
                }}
            }};
        }}

        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {{urls: ["<all_urls>"]}},
                    ['blocking']
        );
        """
    pluginfile = f'proxy_auth_plugin_{index}.zip'
    with zipfile.ZipFile(pluginfile, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)
    options.add_extension(pluginfile)
    return webdriver.Chrome(ChromeDriverManager().install(), options=options)

def close_losers(winner, browsers):
    for browser in browsers:
        if browser != winner:
            browser.close()

def clean_up_extensions():
    for f in glob.glob('proxy_auth_plugin_*.zip'):
        os.remove(f)

proxy_list = [{'ip_address': '', 'port': '', 'username': '', 'password': ''}]

browsers = list()
for i, prox in enumerate(proxy_list):
    browsers.append(spawn_proxy_browser(prox['ip_address'], prox['port'], prox['username'], prox['password'], i))
queue = False
while not queue:
    for sel in browsers:
        if queue:
            pass
        else:
            sel.get('http://direct.playstation.com/en-us/ps5')
            body = sel.find_element_by_tag_name('body')
            if body.get_attribute('class') == 'queue challenge':
                queue = True
                close_losers(sel, browsers)
                clean_up_extensions()
                say('ps5 queue is active')
            elif body.get_attribute('class') == 'softblock':
                say('captcha-challenge block')
                sel.maximize_window()
            else:
                sel.maximize_window()
                time.sleep(5)