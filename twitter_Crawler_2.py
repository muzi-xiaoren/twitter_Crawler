import os
import time
from selenium.common.exceptions import TimeoutException
from manga_downloader import download_media
from driver_init import initialize_driver, cookies_web, get_twitter_name


if __name__ == "__main__":
    user_choice = input('''请输入选项(1/2/3/12/123),回车默认全部下载):
1 - 图片    2 - 视频    3 - GIF动图
'''
) or '123'
    # 初始化浏览器驱动
    driver = initialize_driver()

    # 尝试访问X/Twitter登录页面
    try:
        driver.get('https://x.com/i/flow/login')
    except TimeoutException:
        driver.execute_script('window.stop()')
    driver.set_page_load_timeout(60)

    try:
        driver.get('https://twitter.com')  # 先访问一次目标域名
        cookies_web(driver, "X_cookie.json")
    except:
        print("访问失败，请检查网络连接")
        
    # 访问特定的Twitter页面
    print("访问推特页面中.....")
    target_url = "https://twitter.com/AiNanazi/media"
    driver.get(target_url)
    print("准备获取数据中.....")
    time.sleep(1)

    # 判断target_url是否包含"media"
    is_media = target_url.endswith("/media")

    # 获取Twitter用户名并创建相应的文件夹
    folder = get_twitter_name(driver)
    if not os.path.exists(folder):
        os.makedirs(folder)

    video_folder = os.path.join(folder, "video & gif")
    if "2" in user_choice or "3" in user_choice:
        if not os.path.exists(video_folder):
            os.makedirs(video_folder)

    # 下载图片和视频
    download_media(driver, folder, video_folder, user_choice, is_media)

    # 关闭浏览器
    print(f'共有{len([f for f in os.listdir(folder) if f.endswith('.png')])}张图片')
    if "2" in user_choice or "3" in user_choice:
        print(f'共有{len(os.listdir(video_folder))}个视频')

