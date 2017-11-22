#分享下以前用3写的一款老司机爬虫  地址已经失效了  修改下应该还可以用，来自论坛分享。
#coding:utf-8
import urllib.request
import os 
import re
import time 
import multiprocessing

def open_url(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0')
    response = urllib.request.urlopen(req)
    html = response.read()
    
    return html
      
def second_page(page_url):
    list1 = []
    p = r'<a href="(http://www\.pusiji\.com/play/[^"]+)'
    html = open_url(page_url).decode('utf-8')
    page = re.findall(p, html)
    
    new_page = list(set(page))

    for each in new_page:
        list1.append(each)

    #print(list1)
    return list1

def find_video(url):
    html = open_url(url).decode('utf-8')
    p = r"var data = \'(http://a\.b\.space\.lsjmail\.com/[^']+?.mp4)"

    video_list = re.findall(p, html)
    #print(video_list)
    return video_list

def get_title(url):
    html = open_url(url).decode('utf-8')
    p = r'<title>(.+?)-老司机视频-老司机中文网</title>'
    title = re.findall(p, html)
    title = ''.join(title)
    #print(title)
    return title

def down_video(url):
    title = get_title(url)
    time.sleep(0.5)
    filename = title + '.mp4'
    video_list = find_video(url)
    time.sleep(0.5)
    for video in video_list:
        print('[*]开始下载[%s]' % title)
        urllib.request.urlretrieve(video, filename)
        print('[*]ok![%s]下载结束\n' % title)
        time.sleep(0.5)
            
def main(page):
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    page_url = second_page('http://www.pusiji.com/video/all-flag-new.html?page=%d' % page) 
    time.sleep(0.5)
    for url in page_url:
        pool.apply_async(down_video, (url, ))
    pool.close()
    pool.join()
        
if __name__ == '__main__':
    text = '''
    .-----------------------------.
    |            版权             | 
    |          By：iceH           |
    |      爬取的资源来源于:      |
    |    http://www.pusiji.com    |
    |      本爬虫全自动运行       |
    .-----------------------------.
    '''
    print(text)
    page = int(input('请输入你要爬取哪页的内容:\n'))
    folder = '视频'
    os.mkdir(folder)
    os.chdir(folder)
    main(page)
 
