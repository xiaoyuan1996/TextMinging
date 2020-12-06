from nltk.tokenize import sent_tokenize
import os
import time

source_path = '../../data/processedData/it'
target_path = '../../data/processedData/it2'

# 分句
def sentence_token_nltk(str):
    sent_tokenize_list = sent_tokenize(str)
    return sent_tokenize_list

def place(zi,mu):
    """查询子字符串在大字符串中的所有位置"""
    len1 = len(zi)
    pl = []
    for each in range(len(mu)-len1):
        if mu[each:each+len1] == zi:   #找出与子字符串首字符相同的字符位置
            pl.append(each)
    return pl

def split_point(line):
    result_list = []

    if len(line.split(' | ')) < 3:
        return result_list
    # print(line)
    html, index, text = line.split(' | ', 2)
    sent_list = sentence_token_nltk(text)
    if len(sent_list) < 2:
        result_list.append(line)
        return result_list

    # sentences = [sentence for sentence in sentences if len(sentence) >= 4]
    if len(index.split(':')) < 2:
        return result_list
    begin, end = index.split(':')

    for sentence in sent_list:
        strs = sentence.split(' ')
        if len(strs) < 4:
            continue
        # 子句所有位置
        pos = place(sentence,text)
        for i in pos:
            index_begin = int(begin) + int(i)
            index_end = index_begin + len(sentence)
            result_list.append(html + ' | ' + str(index_begin) + ':' + str(index_end) + ' | ' + sentence + '\n')
    return result_list

def process(lines,file):
    for line in lines:
        result_list = split_point(line)
        for result in result_list:
            with open(os.path.join(target_path, file), 'a', encoding='utf8') as f:
                f.write(result)

def main():
    '''
    str = 'Un piccolo locale, nato come birreria con cucina, propone piatti del territorio preparati con prodotti a chilometro zero (provenienti da micro attività della zona) e materie prime di qualità. Da provare i taglieri di salumi; ampia scelta di birre. Nel periodo estivo è possibile usufruire della terrazza con vista panoramica'
    sent_list = sentence_token_nltk(str)
    position = place(sent_list[1],str)
    print(str[position[0]:position[0]+len(sent_list[1])])'''
    # index1 = len(sent_list[0])
    # index2 = index1 + len(sent_list[1])
    # print(str[index1:index2])
    # print(sent_list)
    files = os.listdir(source_path)
    start = time.time()
    i = 1
    for file in files:
        print('第{}个文件'.format(i))
        print(file)
        i = i + 1
        if not os.path.isdir(file):
            path = os.path.join(source_path, file)
            with open(path, 'r', encoding='utf8') as f:
                lines = f.readlines()
                process(lines, file)

        end = time.time()
        print('Running time: %s Seconds' % (end - start))
        print()
    print()
    print('over')

if __name__ == '__main__':
    main()