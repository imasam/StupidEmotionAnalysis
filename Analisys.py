#############################################
# Analisys.py对爬虫得到数据加以分析
# 以Spider3爬取的数据为例进行分析
#############################################

############################## 引入库函数
#############################  来自开源项目：结巴中文分词 https://github.com/fxsjy/jieba
import jieba
import jieba.analyse


############### 将内容按“.”分词
############### s为待处理文本
def split(s):
    return '.'.join(jieba.cut(s, cut_all=False)).split('.')


############### 基于TF-IDF算法的关键词抽取，抽取前10个关键字
############### s为待处理文本，n为默认抽取量10
def tfidf(s, n=10):
    return jieba.analyse.extract_tags(s, topK=n, withWeight=False, allowPOS=())


############### 基于TextRank算法的关键词抽取，抽取前10个关键字
############### s为待处理文本，n为默认抽取量10
def textrank(s, n=10):
    return jieba.analyse.textrank(s, topK=n, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v'))

# 定义类对应情感字典的每一项，每项有三个属性
class words:
    def __int__(self):
        self.t = ''
        self.a = 0
        self.b = 0


############### 将情感字典中的内容写入字典diction中
############### path为情感字典的路径
def dict(path):
    file = open(path)
    cnt = 0
    while True:
        try:
            text = file.readline().replace('\n', '').split('\t')
            s = text[0]
            tmp = words()
            tmp.t = text[1]
            tmp.a = int(text[2])
            tmp.b = int(text[3])
            diction[s] = tmp
            cnt += 1
            if not text:
                break
        except:
            break
    file.close()


############### 抽取关键字
############### s为待处理文本
def keyword(s):
    print('The keywords of TF-IDF')
    print(tfidf(s, 20))

    print('\nThe keywords of TextRank')
    print(textrank(s, 20))


############### 计算各类情感的权值之和
############### s为待处理文本
def emotion(s):
    a = split(s)

    # 初始化
    p = {'PA': 0,
         'PE': 0,
         'PD': 0,
         'PH': 0,
         'PG': 0,
         'PB': 0,
         'PK': 0,
         'NA': 0,
         'NB': 0,
         'NJ': 0,
         'NH': 0,
         'PF': 0,
         'NI': 0,
         'NC': 0,
         'NG': 0,
         'NE': 0,
         'ND': 0,
         'NN': 0,
         'NK': 0,
         'NL': 0,
         'PC': 0}

    # 计算权值之和
    for x in a:
        try:
            b = diction.get(x)
            if b:
                p[b.t] += b.a
        except:
            continue

    # 降序排列
    return sorted(p.items(), key=lambda d: d[1], reverse=True)


############### 输出情感和对应权值
############### res为按权值排序后的字典，默认输出降序前三位
def output(res, limit=3):
    # print( res )
    cnt = 0

    for key, value in res:
        cnt += 1
        if value == 0:  # 跳过为0的项
            break
        try:
            print(name[key], value) # 输出情感和对应权值
        except:
            continue

        if cnt == limit:    # 达到次数后停止输出
            break


############### 按行分析情感
############### s为待处理文本，limit为循环计数器，res为初始字典，
def calculation(s, limit, res):
    ret = res
    a = split(s)

    # 初始化字典
    p = {'PA': 0,
         'PE': 0,
         'PD': 0,
         'PH': 0,
         'PG': 0,
         'PB': 0,
         'PK': 0,
         'NA': 0,
         'NB': 0,
         'NJ': 0,
         'NH': 0,
         'PF': 0,
         'NI': 0,
         'NC': 0,
         'NG': 0,
         'NE': 0,
         'ND': 0,
         'NN': 0,
         'NK': 0,
         'NL': 0,
         'PC': 0}

    # 计算权值之和
    for x in a:
        try:
            b = diction.get(x)
            if b:
                p[b.t] += b.a
        except:
            continue

    #降序排列
    p = sorted(p.items(), key=lambda d: d[1], reverse=True)

    # 输出PH对应的情感及其权值
    # 此处作该步分析的原因在实验报告中说明
    cnt = 0
    for key, value in p:
        cnt += 1
        if value == 0:
            break
        if key == 'PH':
            print(s, key, value, '\n')
        ret[key] += 1
        if cnt == limit:
            break

    return ret

########################################## 主体部分
# 情感名与代号对应的字典
name = {'PA': '快乐',
        'PE': '安心',
        'PD': '尊敬',
        'PH': '赞扬',
        'PG': '相信',
        'PB': '喜爱',
        'PK': '祝愿',
        'NA': '愤怒',
        'NB': '悲伤',
        'NJ': '失望',
        'NH': '内疚',
        'PF': '思念',
        'NI': '慌张',
        'NC': '恐惧',
        'NG': '羞恼',
        'NE': '烦闷',
        'ND': '憎恶',
        'NN': '贬责',
        'NK': '嫉妒',
        'NL': '怀疑',
        'PC': '惊奇'}

# 读取整个文件，此处来自Spider3爬取内容
s = open('data3.txt').read()

# 写入情感字典
diction = {}
dict('emo_dic1.txt')
dict('emo_dic2.txt')

'''
print('The top 20key words of TF-IDF')
print(tfidf(s, 20))

print('\nThe top 20 key words of TextRank')
print(textrank(s, 20))
'''

keyword(s)  # 输出两种算法抽取的关键字

# 输出总体情感的前5位
print('\nThe top 5 emotion of All text')
output(emotion(s), 5)
print('\n')

s = open('data3.txt')

p = {'PA': 0,
     'PE': 0,
     'PD': 0,
     'PH': 0,
     'PG': 0,
     'PB': 0,
     'PK': 0,
     'NA': 0,
     'NB': 0,
     'NJ': 0,
     'NH': 0,
     'PF': 0,
     'NI': 0,
     'NC': 0,
     'NG': 0,
     'NE': 0,
     'ND': 0,
     'NN': 0,
     'NK': 0,
     'NL': 0,
     'PC': 0}

# 按行计算各情感权值并降序排列，输出其主要情感
print("\nThe paragraphs to be analisysed as PH:")
while True:
    x = s.readline()

    if not x:
        break

    p = calculation(x, 1, p)    # 计算各段情感权值

# 降序排列
p = sorted(p.items(), key=lambda d: d[1], reverse=True)

print("\nFor every paragraph,the top 5 emotions are:")
output(p, 5)   # 输出每个段落情感的前5位


