import json
import time
from download_pic import *
from download_video import *
from json_process import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.common.exceptions import TimeoutException


def media_video():
    global url_list
    logs_raw = driver.get_log("performance")
    logs = [json.loads(lr["message"])["message"] for lr in logs_raw]

    # print(logs)
    def log_filter(log_):
        # if (log_["method"] == "Network.responseReceived" and "json" in log_["params"]["response"]["mimeType"]
        #         and 'UserMedia' in log_["params"]["response"]["url"]):
        #     print(log_["params"]["response"])
        return (
            # is an actual response
                log_["method"] == "Network.responseReceived"
                # json
                and "json" in log_["params"]["response"]["mimeType"]
                and 'UserMedia' in log_["params"]["response"]["url"]
        )

    variants_lists = []
    for log in filter(log_filter, logs):
        request_id = log["params"]["requestId"]
        resp_url = log["params"]["response"]["url"]
        # print(f"Caught {resp_url}")
        res = driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})['body']
        res = json.loads(res)
        # print(res)

        # 提取每个 "variants" 中比特率最大的 URL
        variants = json_value_find(res, "variants")
        if variants not in variants_lists:
            # print(variants)
            variants_lists.append(variants)
            for variant in variants:
                temp = get_max_bitrate_url(variant)
                if temp not in url_list and 'tag=12' in temp:
                    url_list.append(temp)
    # print(url_list)


def download_new(folder, video_folder):
    while len(driver.find_elements(By.CSS_SELECTOR, "div[data-testid='cellInnerDiv']")):
        try:
            for data in driver.find_elements(By.CSS_SELECTOR, "div[data-testid='cellInnerDiv']")[0:7]:
                # print(len(driver.find_elements(By.CSS_SELECTOR, "div[data-testid='cellInnerDiv']")))
                # print(len(data.find_elements(By.TAG_NAME, "img")))    # 调试时使用
                for img in data.find_elements(By.TAG_NAME, "img"):
                    src = img.get_attribute('src')
                    if "profile_images" not in src and 'media' in src:
                        string_list.append(src[:src.find('?')] + "?format=png&name=large")  # &name=large
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
            media_video()
            print('media')
        except BaseException as error:
            print('what?')
            print(str(error))
            continue
    print('')
    get_url_pic(string_list, len(string_list), folder)
    get_url_video(url_list, len(url_list), video_folder)
    print(f'共下载{len(string_list)}张图片,{len(url_list)}个视频')


if __name__ == "__main__":
    # 初始化
    chrome_options = ChromeOptions()
    chrome_options.set_capability(
        "goog:loggingPrefs", {"performance": "ALL"}
    )
    chrome_options.add_argument("window-position=660,0")  # 控制浏览器相对于屏幕的启动位置,便于运行时查看终端输出调试。x,y(0,0)在最左侧,可以根据屏幕调节。
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(5)
    string_list = []
    url_list = []

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
    driver.get("https://twitter.com/misyune12/media")  # 此处修改爬取推文
    print("准备获取图片和视频中.....")
    time.sleep(1)
    name = driver.find_elements(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[2]/div[1]/div/div[1]/div/div/span/span[1]')
    folder = name[0].text.replace('/', '-')  # 防止斜杠视作创建多级文件夹
    print(folder)
    # 创建twitter名称文件夹
    if not os.path.exists(folder):
        os.makedirs(folder)

    video_folder = os.path.join(folder, "video")
    if not os.path.exists(video_folder):
        os.makedirs(video_folder)

    download_new(folder, video_folder)
