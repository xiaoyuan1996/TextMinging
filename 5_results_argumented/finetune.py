import mytools
import os
import jieba
import numpy as np
import pandas as pd
from tqdm import tqdm
from nltk.translate.bleu_score import sentence_bleu,SmoothingFunction,corpus_bleu
# 测试两条语句的bleu
def getBleu(source,target):
    sf7 = SmoothingFunction().method7
    r = sentence_bleu([source], target, weights=(0.25, 0.25, 0.25, 0.25), smoothing_function=sf7)
    return r

def load_raw(html, loc):
    zh_file_name = "../../../data/zhit-0825/" + html
    with open(zh_file_name, encoding='UTF-8') as f:
        source = f.read()
    start, end = loc.split(":")
    start, end = int(start), int(end)
    zh_text = source[start:end]
    return zh_text

def save_to_csv(results, default_path = "submission", return_min = False):

    results = np.array(results)

    results = np.array(list(set([tuple(t) for t in results])))

    results = results[np.lexsort(results[:,::-1].T)[::-1]]

    already_loged_zh = []
    already_loged_ja = []
    sort = []
    for d in tqdm(results):
        d[1] = d[1].replace("../zhit-0825/","").replace("zh/3\\","zh/2020-04-18/").replace("zh/2\\","zh/2020-04-18/")
        d[3] = d[3].replace("../zhit-0825/","")

        log_zh = load_raw(d[1],d[2])
        log_ja = load_raw(d[3],d[4])

        if (log_zh not in already_loged_zh) and (log_ja not in already_loged_ja):
        # if (log_zh not in already_loged_zh):
            sort.append(d)
            already_loged_ja.append(log_ja)
            already_loged_zh.append(log_zh)
    results = np.array(sort)

    # 进行筛选bleu最大的
    if len(results) >30000:
        results = results[:30000, :]

    all_bleu = np.sum([float(tmp) for tmp in results[:10000, 0]])


    data = pd.DataFrame(results, index=None, columns=["bleu","file_source", "location_source","file_target","location_target"])
    data.to_csv("file/bleu_"+default_path+".csv", index=None)

    data = pd.DataFrame(results[:,1:], index=None, columns=["file_source", "location_source","file_target","location_target"])
    data.to_csv("file/"+default_path+".csv", index=None)
    print("Save finished")

    if return_min:
        return results.tolist(), all_bleu, float(results[-1][0])
    else:
        return results.tolist(), all_bleu

ctxs = mytools.load_from_txt("new_dict_lower.txt")
DICT = {}
for ctx in ctxs:
    try:
        zh_, it_ = ctx.replace("\n","").split(" | ")
    except:
        items = ctx.replace("\n","").split(" | ")
        zh_, it_ = items[0], items[1]

    DICT[zh_] = it_

csv_path = "bleu_submission.csv"
data = np.array(pd.read_csv(csv_path)).tolist()

goodwords = mytools.load_from_json("good_words.json")
for goodword in goodwords:
    jieba.add_word(goodword)
new_data = []

for idx,d in tqdm(enumerate(data)):
    zh = load_raw(d[1], d[2])
    it = load_raw(d[3], d[4])

    zh_words = jieba.lcut(zh)
    it_trans = ""
    for zh_word in zh_words:
        if zh_word in DICT.keys():
            it_trans += DICT[zh_word]

    bleu_ = getBleu(it_trans.lower(), it.lower())
    if bleu_ > 0.1:
        new_data.append([
            0.3*bleu_+0.7*d[0], d[1], d[2], d[3], d[4]
        ])
save_to_csv(new_data,"last_result")
sum_new_data = 0
for d in new_data[:10000]:
    sum_new_data += float(d[0])
print("After Optim:", sum_new_data)