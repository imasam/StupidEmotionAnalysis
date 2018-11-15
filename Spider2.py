#############################################
# Spider2.py为爬虫改进版本，爬取“李毅吧”的帖子内容
#############################################


############################## 引入库函数
import http.cookiejar
import urllib.request
import urllib
import re


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


################################## 存储函数
################################## 存储内容至目标文件
################################## data为需处理的内容
def saveFile(data):
    for str2 in data:
        try:
            f_obj.write(str2)
        except:
            continue

################################## 搜索函数
################################## 搜索当前页面中所有的超级链接并做处理
################################## url为需处理的链接，tot为循环次数，mustinclude为必须包含的内容
def download(url, tot, mustinclude):
    oper = makeMyOpener()
    uop = oper.open(url, timeout=1000)
    data1 = uop.read().decode('utf-8', 'ignore')
    a = mustinclude

    if a in data1:
        first = False
        linkre = re.compile('class=\"d_post_content j_d_post_content \">(.+?)</div>')
        # linkre = re.compile('class=\"d_post_content j_d_post_content  clerfix\">(.+?)</div>')

        for x in linkre.findall(data1):
            if first:
                first = False
                continue

            # 将内容中所有空格、换行统一替换成一个换行
            x = x.replace('<br>', '\n').replace('  ', ' ').replace('　　', '　').replace(' ', '\n').replace('　', '\b')\
                          .replace( '\n\n', '\n').replace('\n\n', '\n').replace('\n\n', '\n').replace('\n\n', '\n')\
                          .replace('\n\n', '\n')

            data = ''

            # 跳过因帖子中图片、表情等而产生的其他html标签
            flag = True
            for i in range(0, len(x)):
                if (x[i] == '>' and flag == False):
                    flag = True
                else:
                    if (flag == True):
                        if (i + 1 < len(x) and x[i] == '<' and ((x[i + 1] >= 'a' and x[i + 1] <= 'z')
                            or (x[i + 1] >= 'A' or x[i + 1] <= 'Z'))):
                            flag = False
                        else:
                            data += x[i]
            saveFile(data)

        print('Succeed to write the ', tot, '-th data')
        return 0
    return 1


cnt = 0 #设置计数器
tot = 0
limit = 500
f_obj = open('data1.txt', 'w')

# mustinclude = '武汉大学'
# mustinclude = '新闻'
mustinclude = '李毅'

for i in range(1, 50):
    from collections import deque

    queue = deque()
    visited = set() # 判断是否已访问

    # first = 'http://tieba.baidu.com/f?kw=%D0%C2%CE%C5&fr=ala0&tpl=5?pn='+str(i)
    # first = 'http://tieba.baidu.com/f?ie=utf-8&kw=%E6%AD%A6%E6%B1%89%E5%A4%A7%E5%AD%A6%E5%90%A7?pn='+str(i)
    first = 'http://tieba.baidu.com/f?kw=%E6%9D%8E%E6%AF%85&fr=wwwt&pn=' + str(i)   # 初始地址
    queue.append(first) # 初始地址加入队列

    while queue:
        url = queue.popleft()  # 队首元素出队
        url = url.replace('&amp;', '&')
        visited |= {url}  # 标记为已访问
        print('已经抓取: ', cnt, '个链接', '   正在抓取  ：  ' + url)
        cnt += 1

        if 'http://tieba.baidu.com/p/' in url:
            if download(url, tot, mustinclude):
                continue
            tot += 1
            if tot >= limit:
                break

        urlop = urllib.request.urlopen(url)
        if 'html' not in urlop.getheader('Content-Type'):   # 判断是否是html文本，不是则读取下一条
            continue

        # 避免程序异常中止, 用try..catch处理异常
        try:
            data = urlop.read().decode('utf-8')
        except:
            continue

        linkre = re.compile('href=\"(.+?)\"')   # 通过正则表达式匹配所有href=\" "之间的文本，即超级链接
        for x in linkre.findall(data):
            # 链接符合帖子链接特征，且通过set()保证未爬取过
            if ('first' in x or 'http://tieba.baidu.com/p/' in x) and 'pid' not in x and x[0] == 'h' and x not in visited:
                queue.append(x) # 加入队列
                visited |= {x}  # 加入集合，以标记该元素，避免重复添加
                print('把 ' + x + '加入队列')

        linkre = re.compile('href=\"(.+?)\"')
        for x in linkre.findall(data):
            # 排除“只看楼主”的情况，且链接符合帖子链接特征
            if len(x) > 3 and 'see_lz' not in x and 'pid' not in x and x[0] == '/' and x[1] == 'p' and x[2] == '/':
                x = 'http://tieba.baidu.com' + x    # 补齐相对链接
                if (x not in visited):
                    queue.append(x)
                    visited |= {x}
                    print('把 ' + x + '加入队列')

    if tot >= limit:
        break
f_obj.close()
