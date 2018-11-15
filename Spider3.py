#############################################
# Spider3.py爬虫最终版本，爬取“魏泽西吧”的帖子内容
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

    #帖子发言内容在该html标签内，通过正则表达式匹配每个楼层的发帖内容
    linkre = re.compile('class="d_post_content j_d_post_content ">(.+?)</div>')

    data1 = ''

    #处理获得的内容
    for x in linkre.findall(data):
        #将内容中所有空格、换行统一替换成一个换行
        x = x.replace('<br>', '\n').replace('  ', ' ').replace('　　', '　').replace(' ', '\n').replace('\n\n',
            '\n').replace('\n\n', '\n').replace('\n\n', '\n').replace('\n\n', '\n')

        #跳过因帖子中图片、表情等而产生的其他html标签
        flag = True
        for i in range(0, len(x)):
            if (x[i] == '>' and flag == False):
                flag = True
            else:
                if (flag == True):
                    if (i + 1 < len(x) and x[i] == '<' and ((x[i + 1] >= 'a' and x[i + 1] <= 'z') or
                        (x[i + 1] >= 'A' or x[i + 1] <= 'Z'))):
                        flag = False
                    else:
                        data1 += x[i]

    #将处理过的内容写入文件
    for x in data1:
        try:
            fobj.write(x)
        except:
            continue


################################## 搜索函数
################################## 搜索当前页面中所有的超级链接并做处理
################################## data为需处理的内容，q为队列，s为集合，first为初始地址
def search(data, q, s, first):
    print("Searching for more links...")

    linkre = re.compile('href=\"(.+?)\"')   # 通过正则表达式匹配所有href=\" "之间的文本，即超级链接

    for x in linkre.findall(data):
        #链接符合帖子链接特征，且通过set()保证未爬取过
        if ((first in x or 'http://tieba.baidu.com/p/' in x) and 'pid' not in x and x[0] == 'h' and x not in s):
            q.append(x) # 加入队列
            s |= {x}    # 加入集合，以标记该元素，避免重复添加
            print('Adding ' + x + ' into Queue...')

    #处理相对链接
    linkre = re.compile('href=\"(.+?)\"')
    for x in linkre.findall(data):
        #排除“只看楼主”的情况，且链接符合帖子链接特征
        if (len(x) > 3 and 'see_lz' not in x and 'pid' not in x and x[0] == '/' and x[1] == 'p' and x[2] == '/'):
            x = 'http://tieba.baidu.com' + x    # 补齐相对链接
            if x not in s:
                q.append(x) # 加入队列
                s |= {x}    # 加入集合，以标记该元素，避免重复添加
                print('Adding ' + x + ' into Queue...')


############################################# 伪装浏览器信息
def makeMyOpener(head={
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
}):
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    header = []
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header
    return opener


############################# 爬虫主函数
############################# first为初始地址，number设为默认运行100次
def Spider(first, number = 100):
    q = deque() # 声明双端队列q
    s = set()   # 声明集合{S}
    q.append(first) # 初始地址入队
    s |= {first}    # 初始地址加入集合，以标记该元素，避免重复添加
    cnt = 0 # 设置计数器

    fobj = open('data3.txt', 'w')  # 打开文件data3.txt，准备写入

    while q:    # 在队列不为空时
        url = q.popleft()   # 获取队首
        url = url.replace('&amp;', '&') #地址转译
        print('I\'m searching #', cnt, ' website: ', url)   #输出爬取信息
        cnt = cnt + 1  # 计数器增加
        # 搜索次数达到则结束程序
        if cnt == number:
            break

        oper = makeMyOpener()
        urlop = oper.open(url, timeout = 1000)    # 设置超时避免假死

        if 'html' not in urlop.getheader('Content-Type'):   # 判断是否是html文本，不是则读取下一条
            continue
        try:
            data = urlop.read().decode('utf-8') # 尝试用utf-8解码
        except:
            continue

        '''
        # 判断当前网页是否符合我们的需要
        if '魏则西' not in data:
        #if 'WE' not in data:
            continue
        '''

        download(data, fobj)  # 运行下载函数
        search(data, q, s, first)  # 运行搜索函数

    print("Searching finished! I have got ", cnt, '/', number, 'websites')  # 运行结束后输出提示信息


############################################# 运行爬虫，搜索初始地址
Spider("http://tieba.baidu.com/f?kw=%E9%AD%8F%E5%88%99%E8%A5%BF&ie=utf-8")  #魏则西吧
#Spider("https://tieba.baidu.com/f?kw=%B1%B3%B9%F8&fr=ala0&tpl=5")  #背锅吧

