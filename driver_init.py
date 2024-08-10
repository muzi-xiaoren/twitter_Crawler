import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions


def initialize_driver():
    # 初始化Chrome浏览器驱动
    options = ChromeOptions()
    options.set_capability(
        "goog:loggingPrefs", {"performance": "ALL"}
    )

    # # 启用无头浏览器模式
    # options.add_argument("--headless")
    # options.add_argument("--disable-gpu")  # 禁用GPU加速
    # options.add_argument("--window-size=1920x1080")  # 设置窗口大小，防止某些元素不可见

    # 不启用无头模式时开启，调式代码或者看报错的时候使用。
    options.add_argument("window-position=660,0")

    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(5)
    return driver


def cookies_web(driver, cookie_path):
    # 设置浏览器的cookie
    print("设置cookie中.....")
    cookies = json.load(open(cookie_path, 'r'))
    for cookie in cookies:
        driver.add_cookie(cookie)


def get_twitter_name(driver):
    # 获取Twitter用户的名称
    name = driver.find_elements(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div/div/div/div/div/div[2]/div/h2/div/div/div/div/span[1]/span/span[1]')
    folder = name[0].text.replace('/', '-')  # 防止斜杠视作创建多级文件夹

    return folder