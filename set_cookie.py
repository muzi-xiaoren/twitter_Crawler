import json
import time
from selenium import webdriver

# 生成cookies
browser = webdriver.Chrome()

try:
    browser.get("https://x.com/i/flow/login") # https://x.com/i/flow/login 
    time.sleep(30)  # 30s内登录等待退出

finally:
    dictCookies = browser.get_cookies()
    jsonCookies = json.dumps(dictCookies)
    print(jsonCookies)
    with open('X_cookie.json', 'w') as f:
        f.write(jsonCookies)
    browser.quit()
