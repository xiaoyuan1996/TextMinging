import os
import time

source_path = '../../data/processedData/it2'
target_path = '../../data/processedData/it4'

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
    html, index, text = line.split(' | ', 2)

    if len(index.split(':')) != 2:
        return result_list
    # 去掉位置不对的
    begin, end = index.split(':')
    try:
        if (int(end)-int(begin)-len(text)) > 5:
            return result_list
    except:
        return result_list

    word_list = text.split(' ')
    if len(word_list) <= 9:
        result_list.append(line)
    else:
        sentence = ''
        for i in range(len(word_list)):
            sentence = sentence + word_list[i]+' '
            if (i+1) % 9 == 0 or (i+1) == len(word_list):
                sentence = sentence.strip()
                strs = sentence.split(' ')
                if len(strs) < 4:
                    continue
                # 子句所有位置
                pos = place(sentence, text)
                for i in pos:
                    index_begin = int(begin) + int(i)
                    index_end = index_begin + len(sentence)
                    result_list.append(html + ' | ' + str(index_begin) + ':' + str(index_end) + ' | ' + sentence + '\n')
                sentence = ''
    return result_list

def process(lines,file):
    for line in lines:
        result_list = split_point(line)
        for result in result_list:
            with open(os.path.join(target_path, file), 'a', encoding='utf8') as f:
                f.write(result)

def main():
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