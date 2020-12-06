import re
import random

# 计算一段字符在一大段字符中的索引
def calcIndexForPiece(queryWord, sourceWord):
    start_end = [match.span() for match in re.finditer(queryWord,sourceWord)]
    start,end = random.choice(start_end)
    return start,end

#################################################################
# 对每一行进行过滤
filterMap = [i for i in
             " :qwertyuioplkjhgfdsazxcvbnmQWERTYUIOPLKJHGFDSAZXCVBNM/;'[]!@#$%^&*（）『』()`?>×<\"}{}\■】【|=-─+_+-*/~0123456789\t♪～☆★◆"]
def filterForLine(line):
    # 按字切割

    new_line = ""
    for item in line:
        if item not in filterMap:
            new_line += item
        else:
            new_line += " "
    # 裁剪成一个个句子
    new_lines = []
    for i in new_line.split(" "):
        if (i != "") and (len(i)>=10):
            for ii in i.split("。"):
                if (ii != ""):
                    new_lines.append(ii)
    return new_lines

if __name__=="__main__":
    query = "aaa"
    source = "asdeaaasssaaa"
    start,end = calcIndexForPiece(query,source)
    print(start,end)

    # start_end = [match.span() for match in re.finditer(query,source)]
    # print(start_end)