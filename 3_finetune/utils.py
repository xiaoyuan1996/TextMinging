import re
import fasttext
import fasttext.util
import time
import numpy as np
from nltk.corpus import stopwords         #停用词
from nltk.tokenize import word_tokenize   #分词
from nltk.stem import PorterStemmer       #词干化
from nltk.stem import WordNetLemmatizer   #词形还原
stop_words = set(stopwords.words('italian'))  #意大利停用分词集合
ps = PorterStemmer()
pat1=re.compile(r'[\u00e0-\u00ff]+')

# start = time.time()
# model = fasttext.load_model("utils/cc.it.300.bin")
# end = time.time()
# print("load fasttext model finished in {} s".format(end-start))

def get_str_embed(string):
    embeding = []
    for word in string:
        embeding.append(np.array(model.get_word_vector(word)))
    embeding = np.mean(embeding, axis=0)
    return embeding

def cos_sim(vector_a, vector_b):
    """
    计算两个向量之间的余弦相似度
    :param vector_a: 向量 a
    :param vector_b: 向量 b
    :return: sim
    """
    vector_a = np.mat(vector_a)
    vector_b = np.mat(vector_b)
    num = float(vector_a * vector_b.T)
    denom = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
    cos = num / denom
    sim = 0.5 + 0.5 * cos
    return sim

def cmp_str_cos_sim(str1, str2):
    str1_emb = get_str_embed(str1)
    str2_emb = get_str_embed(str2)
    sim = cos_sim(str1_emb, str2_emb)
    return sim

def replace_all_blank(value):
    """
    去除value中的所有非字母内容，包括标点符号、空格、换行、下划线等
    :param value: 需要处理的内容
    :return: 返回处理后的内容
    """
    # \W 表示匹配非数字字母下划线
    result = re.sub('\W+', ' ', value).replace("_", ' ')

    if (len(value)-len(result)) <= 0.3*len(value):
        return result
    else:
        return "_"


# 判断句子是中文还是日文
def detect_sentence_la(sentence):
    p = re.compile(r'[\u3040-\u309F\u30A0-\u30FF\uAC00-\uD7A3]')
    tmp = p.findall(sentence)
    if len(tmp) >1:
        return 'ja'
    else:
        return 'zh'



def save_decision(ctx, lang):
    # 进行符号过滤
    ctx = replace_all_blank(ctx)

    # 如果句子中的字符小于5的话，直接返回None
    if len(ctx.split())<=5 and lang=='it':
        return None
    if len(ctx)<=5 and lang=='zh':
        return None


    # # 在指定语音和实际语言不一样时 返回None
    # if detect_sentence_la(ctx) != lang:
    #     return None

    return ctx

def txt_preprocess(txt, lang='zh'):
    """
    数据预处理
    :param txt: 传进来的txt行内容
    :return: 返回为一个二维数组
    """
    # 去重
    txt = set(txt)

    clear_txt = []
    # 分离 逐个处理
    for text in txt:
        try:
            # 分割
            route, pos, ctx =  text.replace("\n","").split(" | ")

            # 决定要保存与否 以及保存的内容
            ctx = save_decision(ctx, lang)
            if ctx is not None:
                clear_txt.append([route.replace(" ",""), pos, ctx])

        # 防止意外情况
        except:
            pass
    return clear_txt


import mytools
# 读取字典
def readDict(path = "new_dict.txt"):
    print("Reading Directory ...")

    # 读取中译日词典
    ctxs = mytools.load_from_txt(path)

    # 解析每一条并保转换为json形式
    directory = {}
    for ctx in ctxs:
        try:
            source, target = ctx.replace("\n","").split(" | ")
            directory[source] = target
        except:
            pass


    print("Directory load completed .")
    return directory

# 查询单个单词
def queryWord(dict, source):
    if source in dict.keys():
        return dict[source]
    else:
        return '*'

# 查询整个中文句子
import jieba
def querySentence(dict, source):
    # 对每个句子进行分割，成token
    # tokens = source.split(" ")
    word_tokens = word_tokenize(source)  # 分词

    # filtered_sentence = [w for w in word_tokens if w not in stop_words]  # 去停用词
    filtered_sentence = [w for w in word_tokens]  # 去停用词

    filtered_sentence = [word.lower() for word in filtered_sentence]

    tokens = [ps.stem(w) for w in filtered_sentence]

    # 对句子进行简单的拼接
    target = ""
    for token in tokens:
        target += queryWord(dict, token)+""

    return target

def getbleu_replace(source,target):
    same_len = len(set(source) & set(target))
    return same_len

# TODO：核心代码 计算两个话的相似度
from nltk.translate.bleu_score import sentence_bleu,SmoothingFunction,corpus_bleu
from nltk.tokenize import word_tokenize
sf7 = SmoothingFunction().method7

def compute_item_score(item1, item2):
    """
    计算两句话的相似度
    :param item1: 中文句子1
    :param item2: 日语句子2
    :return: 相似度评分
    """
    # 进行分解， 生成词汇池

    score = sentence_bleu([item1], item2, weights=(0.25, 0.25, 0.25, 0.25), smoothing_function=sf7)

    return score
#
# item1 = "一"
# item2 = "一二"
# score = compute_item_score(item1,item2)
# print(score)

#0.7386970545564772 0.3873397281631655
#0.3291473411068133 0.34031521116081387


if __name__=="__main__":
    def get_str_embed_bk(string):
        embeding = []
        for word in string:
            embeding.append(np.array(model.get_word_vector(word)))
        embeding = np.mean(embeding, axis=0)
        return embeding


    def cos_sim_bk(vector_a, vector_b):
        """
        计算两个向量之间的余弦相似度
        :param vector_a: 向量 a
        :param vector_b: 向量 b
        :return: sim
        """
        vector_a = np.mat(vector_a)
        vector_b = np.mat(vector_b)
        num = float(vector_a * vector_b.T)
        denom = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
        sim = num / denom
        # sim = 0.5 + 0.5 * sim
        return sim


    def cmp_str_cos_sim_bk(str1, str2):
        str1_emb = get_str_embed_bk(str1)
        str2_emb = get_str_embed_bk(str2)
        sim = cos_sim_bk(str1_emb, str2_emb)
        return sim

    def process(item1, item2):
        print("-----------------------------")
        print(item1)
        print(item2)
        item1 = word_tokenize(item1)
        item1 = [word.lower() for word in item1]

        item2 = word_tokenize(item2)
        item2 = [word.lower() for word in item2]

        embed_score = cmp_str_cos_sim_bk(item1, item2)
        bleu_score = sentence_bleu([item1], item2, weights=(0.25, 0.25, 0.25, 0.25), smoothing_function=sf7)

        print("embed_score:",embed_score,"  bleu_score:",bleu_score)


    start = time.time()
    model = fasttext.load_model("../../dl-sim/utilize/cc.it.300.bin")
    end = time.time()
    print("load fasttext model finished in {} s".format(end-start))


    str1 = "死者尊严何在？意公墓员工在陵园做饭烧烤引众怒"
    str2 = "Il sottotitolo deve essere utilizzato per gli h2/h3 quindi i sottotitoli o titoli dei paragrafi. Questo è un"

    Dict = readDict(path="new_dict.txt")
    str1 = querySentence(Dict, str1)

    process(str1, str2)