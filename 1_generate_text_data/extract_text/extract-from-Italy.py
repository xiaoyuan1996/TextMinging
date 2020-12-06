from bs4 import BeautifulSoup
import re
import os
import time
import langid

source_path = '../../0_data/zhit-0825/it'
target_path = '../../0_data/processedData/it'

# 查找位置
def place(zi,mu):
    """查询子字符串在大字符串中的所有位置"""
    len1 = len(zi)
    pl = []
    for each in range(len(mu)-len1):
        if mu[each:each+len1] == zi:   #找出与子字符串首字符相同的字符位置
            pl.append(each)
    return pl

# 写入文件
def write_file(strings,html,path,file):
    for str in strings:
        # 判断语言
        language = langid.classify(str.lower())[0]
        if language != 'it':
            continue
        # 去除首尾空格
        str = str.strip()
        strs = str.split(' ')
        if len(strs) < 4:
            continue
        # print(str)
        # str中包含英文括号时无法识别
        '''
        for a in re.finditer(str, html):
            # 位置
            position = repr(a.span()[0]) + ':' + repr(a.span()[1])
            line = path + ' | ' + position + ' | ' + str + '\n'
            with open(os.path.join(target_path, file.replace('html', 'txt')), 'a', encoding='utf8') as f:
                f.writelines(line)
        '''
        pos = place(str, html)
        for i in pos:
            position = repr(i) +':'+ repr((i+len(str)))
            line = path + ' | ' + position + ' | ' + str + '\n'
            with open(os.path.join(target_path, file.replace('html', 'txt')), 'a', encoding='utf8') as f:
                f.writelines(line)

# 处理操作
def process(html,file,path):
    print(file)
    # 将英文括号变成中文括号
    # html = re.sub("\(", "（", html)
    # html = re.sub("\)", "）", html)
    # html = re.sub("\*", " ", html)
    # 将|换成+
    # html = re.sub("\|", " ", html)
    soup = BeautifulSoup(html, 'lxml')
    [s.extract() for s in soup('script')]
    # 还有title中的文本
    # title_string = soup.title.strings
    # write_file(title_string, html, path, file)
    # 文本集合
    # strings = set(soup.body.strings)
    strings = set(soup.strings)
    write_file(strings, html, path, file)

def main():
    files = os.listdir(source_path)
    start = time.time()
    i = 1
    for file in files:
        print('第{}个文件'.format(i))
        i = i+1
        if not os.path.isdir(file):
            path = os.path.join(source_path, file)
            with open(path, 'r', encoding='utf8') as f:
                html = f.read()
                process(html,file,path)
        end = time.time()
        print('Running time: %s Seconds' % (end - start))
        print()
    print()
    print('over')

if __name__ == '__main__':
    main()





