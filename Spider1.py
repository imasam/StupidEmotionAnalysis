#############################################
# Spider1.py为爬虫初步版本，爬取百度首页未处理的html内容
#############################################

############################## 引入库函数
import http.cookiejar
import urllib.request
import urllib
import re
from collections import deque

#################### 下载函数
#################### 下载data数据到fobj打开的文件里
#################### data为需处理的内容，fobj为写入的目标文件
def download(data, fobj):
    print("Downloading...")
    for x in data:
        try:
            fobj.write(x)
        except:
            continue


################## 检查新搜到的网页网址x是否需要入队
################## data为需处理的内容，s为集合用以判断是否重复
def check(x, s):
    if x not in s and 'http' in x:  # 判断是否在集合{S}中以及是否是一个http的链接
        return True
    return False


################################## 搜索函数
################################## 搜索当前页面中所有的超级链接并做处理
################################## data为需处理的内容，q为队列，s为集合，first为初始地址
def search(data, q, s):
    print("Searching for more links...")

    linkre = re.compile('href=\"(.+?)\"')   # 通过正则表达式匹配所有href=\" "之间的文本，即超级链接

    for x in linkre.findall(data):
        if check(x, s):  # 检查该链接是否符合要求
            q.append(x)  # 加入队列
            s |= {x}  # 加入集合，以标记该元素，避免重复添加
            print('Adding ' + x + ' into Queue...')


############################# 爬虫主函数
############################# first为初始地址，number设为默认运行100次
def Spider(first, number = 100):
    q = deque() # 声明双端队列q
    s = set()   # 声明集合{S}
    q.append(first) # 初始地址入队
    s |= {first}    # 初始地址加入集合，以标记该元素，避免重复添加
    cnt = 0 # 设置计数器

    fobj = open('data1.txt', 'w')  # 打开文件data2.txt，准备写入

    while q:  # 在队列不为空时
        url = q.popleft()   # 获取队首
        url = url.replace('&amp;', '&') # 地址转译
        print('I\'m searching #', cnt, ' web site: ', url)  # 输出爬取信息
        cnt = cnt + 1  # 计数器增加
        # 搜索次数达到则结束程序
        if cnt == number:
            break

        urlop = urllib.request.urlopen(url)  # 打开网页

        if 'html' not in urlop.getheader('Content-Type'):   # 判断是否是html文本，不是则读取下一条
            continue
        try:
            data = urlop.read().decode('utf-8') # 尝试用utf-8解码
        except:
            continue

        download(data, fobj)  # 运行下载函数
        search(data, q, s)  # 运行搜索函数

    print("Searching finished! I have got ", cnt, '/', number, 'websites')  # 运行结束后输出提示信息


############################################# 运行爬虫，搜索初始地址
Spider("http://www.baidu.com")  # 运行爬虫搜索初始地址http://www.baidu.com
