import os
import requests
import threading


img_connections = 10  # 定义最大线程数,可根据网速修改
img_sema = threading.BoundedSemaphore(img_connections)  # 或使用Semaphore方法
video_connections = 3  # 定义最大线程数,可根据网速修改
video_sema = threading.BoundedSemaphore(video_connections)  # 或使用Semaphore方法


def download_pic(src, name):
    img_sema.acquire()  # 加锁，限制线程数
    image_name = src[28:43] + ".png"
    image_path = os.path.join(name, image_name)

    if os.path.exists(image_path):
        print(f'{image_name} already exists.')
        img_sema.release()  # 解锁
        return

    print(f'{image_name} is downloading')

    while True:
        try:
            response = requests.get(src)
            if response.status_code == 200:
                break  # 如果状态码为200，跳出循环
        except requests.exceptions.RequestException:
            print("发生错误:重新连接")

    with open(image_path, 'wb') as f:
        f.write(response.content)
    img_sema.release()  # 解锁


def download_video(src, name):
    # 下载视频并保存到指定文件夹
    video_sema.acquire()  # 加锁，限制线程数
    video_name = src.split("/")[-1].split("?")[0]
    video_path = os.path.join(name, video_name)

    if os.path.exists(video_path):
        print(f'{video_name} already exists.')
        video_sema.release()  # 解锁
        return

    print(f'{video_name} is downloading')

    while True:
        try:
            response = requests.get(src)
            if response.status_code == 200:
                with requests.get(src, stream=True) as r:
                    with open(video_path, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                break  # 如果状态码为200，跳出循环
        except requests.exceptions.RequestException:
            print("发生错误:重新连接")

    video_sema.release()


