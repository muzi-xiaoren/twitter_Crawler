import json
import time
from download import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.common.exceptions import TimeoutException


def download_new(name):
    while len(driver.find_elements(By.CSS_SELECTOR, "div[data-testid='cellInnerDiv']")):
        try:
            for data in driver.find_elements(By.CSS_SELECTOR, "div[data-testid='cellInnerDiv']")[0:7]:
                # print(len(driver.find_elements(By.CSS_SELECTOR, "div[data-testid='cellInnerDiv']")))
                # print(len(data.find_elements(By.TAG_NAME, "img")))    # 调试时使用
                for img in data.find_elements(By.TAG_NAME, "img"):
                    src = img.get_attribute('src')
                    if "profile_images" not in src and 'media' in src:
                        string_list.append(src[:src.find('?')] + "?format=png&name=large")   # &name=large
                driver.execute_script(
                    """
                    var dataElements = document.querySelectorAll("div[data-testid='cellInnerDiv']");
                    if(dataElements.length > 0) {
                        dataElements[0].remove();
                    }
                    """)
                time.sleep(0.5)
                if len(driver.find_elements(By.CSS_SELECTOR, "div[data-testid='cellInnerDiv']")) == 0:
                    time.sleep(2)
                print("next", end=' ')
        except BaseException as error:
            print('what?')
            print(str(error))
            continue
    print('')
    get_url(string_list, len(string_list), name)
    print(f'共下载{len(string_list)}张图片')


if __name__ == "__main__":
    # 初始化
    chrome_options = ChromeOptions()
    chrome_options.add_argument("window-position=660,0")  # 控制浏览器相对于屏幕的启动位置,便于运行时查看终端输出调试。x,y(0,0)在最左侧,可以根据屏幕调节。
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(5)
    string_list = []

    try:
        driver.get('https://twitter.com/i/flow/login')
    except TimeoutException:
        driver.execute_script('window.stop()')
    driver.set_page_load_timeout(60)

    # 设置cookie
    print("设置cookie中.....")
    cookies = json.load(open("twitter_cookie.json", 'r'))
    for cookie in cookies:
        driver.add_cookie(cookie)

    print("访问推特页面中.....")
    driver.get("https://twitter.com/___OTINTIN/media")  # 此处修改爬取推文
    print("准备获取图片中.....")
    time.sleep(1)
    name = driver.find_elements(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[2]/div[1]/div/div[1]/div/div/span/span[1]')
    name = name[0].text
    # 创建twitter名称文件夹
    if not os.path.exists(name):
        os.makedirs(name)
    download_new(name)
