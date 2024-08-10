import os
import time
import json
import queue
import requests
import threading
from download_method import download_pic, download_video
from selenium.common.exceptions import InvalidArgumentException
from json_process import json_value_find, get_max_bitrate_url
from selenium.webdriver.common.by import By


def url_producer(driver, q, user_choice, is_media):
    # 生产者线程函数，抓取图片URL并放入队列
    while len(driver.find_elements(By.CSS_SELECTOR, "div[data-testid='cellInnerDiv']")):
        try:
            for data in driver.find_elements(By.CSS_SELECTOR, "div[data-testid='cellInnerDiv']")[0:7]:
                # print(len(driver.find_elements(By.CSS_SELECTOR, "div[data-testid='cellInnerDiv']")))
                # print(len(data.find_elements(By.TAG_NAME, "img")))    # 调试时使用
                if "1" in user_choice:
                    for img in data.find_elements(By.TAG_NAME, "img"):
                        src = img.get_attribute('src')
                        if "profile_images" not in src and 'media' in src:
                            # print(src)
                            q.put(src[:src.find('?')] + "?format=png&name=large")
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
            media_video(driver, q, user_choice, is_media)
            print('media')
        except BaseException as error:
            print('what?')
            print(str(error))
            continue
    q.join()
    print('')
    q.put(None)  # 生产者完成后放入停止信号
    driver.quit()


def url_consumer(q, folder, video_folder):
    # 消费者线程函数，从队列中取出URL并下载图片或视频
    while True:
        src = q.get()
        if src is None:
            break
        if "mp4" not in src:
            thread = download_thread_png(src, folder)
        else:
            thread = download_thread_video(src, video_folder)
        q.task_done()
        # 如果队列为空，等待当前线程完成
        if q.empty():
            thread.join()


def download_thread_png(src, folder):
    # 创建线程下载图片
    thread = threading.Thread(target=download_pic, args=(src, folder))
    thread.start()
    return thread


def download_thread_video(src, video_folder):
    # 创建线程下载视频
    thread = threading.Thread(target=download_video, args=(src, video_folder))
    thread.start()
    return thread


def media_video(driver, q, user_choice, is_media):
    # 从浏览器日志network中提取视频URL
    logs_raw = driver.get_log("performance")
    logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
    # print(logs)
    def log_filter(log_):
        # if (log_["method"] == "Network.responseReceived" and "json" in log_["params"]["response"]["mimeType"]
        #         and 'UserMedia' in log_["params"]["response"]["url"]):
        #     print(log_["params"]["response"])
        url_keyword = 'UserMedia' if is_media else 'UserTweets'
        return (
            log_["method"] == "Network.responseReceived"
            and "json" in log_["params"]["response"]["mimeType"]
            and url_keyword in log_["params"]["response"]["url"]
        )

    variants_lists = []
    for log in filter(log_filter, logs):
        request_id = log["params"]["requestId"]
        resp_url = log["params"]["response"]["url"]
        # print(f"Caught {resp_url}")
        res = driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})['body']
        res = json.loads(res)
        # print(res)

        all_variants = json_value_find(res, "variants")
        # print(all_variants)
        for variants in all_variants:
            if variants not in variants_lists:
                variants_lists.append(variants)
                temp = get_max_bitrate_url(variants)
                if "2" in user_choice:
                    if not any(item == temp for item in list(q.queue)) and 'pu' in temp:
                        # print(temp)
                        q.put(temp)
                if "3" in user_choice:
                    if not any(item == temp for item in list(q.queue)) and 'pu' not in temp:
                        # print(temp)
                        q.put(temp)


def download_media(driver, folder, video_folder, user_choice, is_media):
    # 下载Twitter页面中的图片和视频
    q = queue.Queue()

    producer_thread = threading.Thread(target=url_producer, args=(driver, q, user_choice, is_media))
    consumer_thread = threading.Thread(target=url_consumer, args=(q, folder, video_folder))

    producer_thread.start()
    consumer_thread.start()

    producer_thread.join()
    consumer_thread.join()

