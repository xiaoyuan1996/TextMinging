from nltk.corpus import stopwords         #停用词
from nltk.tokenize import word_tokenize   #分词
from nltk.stem import PorterStemmer       #词干化
from nltk.stem import WordNetLemmatizer   #词形还原
from utils import utils
import os, mytools
from tqdm import tqdm
import re
import jieba
import opencc
t2s = opencc.OpenCC('t2s')

lang = "it"

if lang == "it":
    Dict = utils.readDict(path="utils/filter_vocab.txt")

stop_words = set(stopwords.words('italian'))  #意大利停用分词集合
ps = PorterStemmer()
pat1=re.compile(r'[\u00e0-\u00ff]+')


def replace_all_blank(value):
    """
    去除value中的所有非字母内容，包括标点符号、空格、换行、下划线等
    :param value: 需要处理的内容
    :return: 返回处理后的内容
    """
    # \W 表示匹配非数字字母下划线
    remove_words = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890"
    result = re.sub('\W+', '', value).replace("_", '')

    result = re.sub(pat1, '', result)

    for r in remove_words:
        if r in result:
            result = result.replace(r, "")
    return result

def save_decision(ctx, lang):
    # 进行符号过滤
    ctx = replace_all_blank(ctx)

    filted_results = t2s.convert(ctx)
    return filted_results

if __name__ == "__main__":
    file_name = "sorted_data/sorted_"+lang+".txt"
    ctxs = mytools.load_from_txt(file_name)

    filted_results = []
    for ctx in tqdm(ctxs):
        try:
            html, location, text = ctx.split(" | ")

            if lang == "it":
                word_tokens = word_tokenize(text)  # 分词

                filtered_sentence = [w for w in word_tokens if w not in stop_words]  # 去停用词

                filtered_sentence = [word.lower() for word in filtered_sentence]

                stem_words = [ps.stem(w) for w in filtered_sentence]

                text = " ".join(stem_words)

                text = utils.querySentence(Dict, text)


            # 决定要保存与否 以及保存的内容
            text = save_decision(text, lang)
            # print(text)
            if text is not None:
                if len(text)>=5:
                    print(text)
                    filted_results.append(
                        {
                        "html": html.replace("data/it\\","../zhit-0825/it/2020-04-17/").replace("zh/2020-04-18/","../zhit-0825/zh/2020-04-18/"),
                        "location": location,
                        "text": text
                        }
                    )
        except:
            pass
    mytools.save_to_json(filted_results, file_name.replace("sorted_data","filted_data").replace("txt","json"))