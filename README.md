# twitter_Crawler
推特爬虫/X/twitter


#### 前排提示：第一次运行的话，浏览器可能启动比较慢，原因未知。可以久等一会。


### 1.<a href="#twitter_Crawler_2"> twitter_Crawler_2 下载图片使用</a>


### 2.<a href="#twitter_Crawler_3"> twitter_Crawler_3 下载图片和视频使用 </a>


### 3.<a href="#problems"> 目前存在的问题</a>


# 注意事项


## 第一步获取cookie
1. 使用的方法是运行 ***set_cookie.py*** 。然后在30s在网页上登陆推特。


2. 等待页面关闭。就能获取到用来登陆的cookie，会以 ***twitter_cookie.json*** 保存在文件夹中。


## 一些其他说明
1. 由于推特页面是动态加载的，所有使用selenium库对浏览器进行操作，来刷新页面，并获取页面中图片的下载地址，以及在network中获取视频和GIF的地址。最后用request请求下载到本地。


2. 下载使用线程锁，一次同时下载10张图片和3个视频。如果对网速很有自信。可以在 ***download_pic.py和download_video.py*** 中对 ***max_connections*** 的值进行更改


## <a id="twitter_Crawler_2">twitter_Crawler_2</a>
1. 在61行修改页面地址。直接运行即可。


2. 对于可修改的页面，主页和媒体都是可以爬取的。


## <a id="twitter_Crawler_3">twitter_Crawler_3 下载图片和视频使用</a>
1. 在109行修改页面地址。直接运行即可


2. 如果想要下载GIF，请在46行删掉或者注释 ***''tag=12' in temp'*** 这段代码


## <a id="problems"> 目前存在的问题</a>
1. 当media页面中的部分含有多个内容时，只能下载封面这一张内容。目前没有想到好的解决方法。


