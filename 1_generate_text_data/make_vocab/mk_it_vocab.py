import mytools
import os,re
from nltk.corpus import stopwords         #停用词
from nltk.tokenize import word_tokenize   #分词
from nltk.stem import PorterStemmer       #词干化
from nltk.stem import WordNetLemmatizer   #词形还原
from tqdm import tqdm

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
    result = re.sub('\W+', ' ', value).replace("_", ' ').replace(r"\u", " ")

    result = re.sub(pat1, '', result)

    if (len(value)-len(result)) <= 0.3*len(value):
        return result
    else:
        return "_"
ctxs = mytools.load_from_txt("../filter_data/sorted_data/sorted_it.txt")


counts = {}
for ctx in tqdm(ctxs):
    html, location, text = ctx.replace("\n", "").split(" | ")

    text = replace_all_blank(text)
    word_tokens = word_tokenize(text) #分词
    # filtered_sentence = [w for w in word_tokens if w not in stop_words] #去停用词
    # filtered_sentence = [word.lower() for word in filtered_sentence]
    # stem_words = [ps.stem(w) for w in filtered_sentence]

    stem_words = [word.lower() for word in word_tokens]

    for w in stem_words:
        counts[w] = counts.get(w, 0) + 1
cw = sorted([(count, w) for w, count in counts.items()], reverse=True)
cw = [w[1]+" | "+str(w[0])+"\n" for w in cw]
mytools.log_to_txt(cw, "all_it_vocab.txt")
