import os
import pandas as pd
import numpy as np
from tqdm import tqdm
import time
from nltk.tokenize import word_tokenize   #分词

def save_to_csv(results, default_path = "submission", return_min = False):

    results = np.array(results)

    results = np.array(list(set([tuple(t) for t in results])))

    results = results[np.lexsort(results[:,::-1].T)[::-1]]

    already_loged_zh = []
    already_loged_ja = []
    sort = []
    for d in results:
        d[1] = d[1].replace("../zhit-0825/","").replace("zh/3\\","zh/2020-04-18/").replace("zh/2\\","zh/2020-04-18/")
        d[3] = d[3].replace("../zhit-0825/","")

        log_zh = d[1] + d[2]
        log_ja = d[3] + d[4]

        if (log_zh not in already_loged_zh) and (log_ja not in already_loged_ja):
        # if (log_zh not in already_loged_zh):
            sort.append(d)
            already_loged_ja.append(log_ja)
            already_loged_zh.append(log_zh)
    results = np.array(sort)

    # for d in results:
    #     d[3] = d[3].replace("25/it/", "it/")

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

def read_text_from_file(route, location):
    start, end = location.split(":")
    start, end = int(start), int(end)
    with open(route, encoding='UTF-8') as f:
        source = f.read()[start:end]
    return source

remove_map = [
"ong", "calabria", "reggio", "bbc", "SIVIGLIA".lower(), "RPCT".lower(), "srl", "ceo", "srls", "snc", "UNESCO".lower(),
"mai", "abc", "pil", "staff", "dovevamo", "pil", "png", "soccer", "REGGIO".lower(), "aureato", "dovremo", "emersi",
"finora", "scusami", "staffe", "steel", "vediamo", "fmi", "quando", "avveniva"
]

# Read data
data = np.array(pd.read_csv("../3_finetunefile/bleu_after_optim.csv"))
data =  data.tolist()

new_data = []
for d in tqdm(data):
    it_text = read_text_from_file("../0_data/zhit-0825/" + d[3], d[4])

    flag = False
    all_words = word_tokenize((it_text.lower()))
    for word in remove_map:
        if word in all_words:
            flag = True

    if not flag:
        new_data.append(d)

save_to_csv(new_data, "acronym")