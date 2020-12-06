import randomFinding
import mytools
import os,time,random
from nltk.translate.bleu_score import sentence_bleu,SmoothingFunction,corpus_bleu
sf7 = SmoothingFunction().method7
import numpy as np
import pandas as pd

it_json = mytools.load_from_json("../../data/last_data/modified_it.json")
zh_json = mytools.load_from_json("../../data/last_data/modified_zh.json")

def getSavedCsv():
    data = np.array(pd.read_csv("file/bleu_submission.csv"))
    return data.tolist()

all_results = []
if os.path.exists("file/bleu_submission.csv"):
    all_results = getSavedCsv()


idx = 0
min_score = 0.45
start_time = time.time()
while True:
    it = random.choice(it_json)
    it_text = it['text']

    zh = random.choice(zh_json)
    zh_text = zh['text']

    try:
        score = sentence_bleu([it_text], zh_text, weights=(0.33, 0.33, 0.34), smoothing_function=sf7)
    except:
        continue

    if score > min_score:
        all_results.append(
            [score,
             zh['html'],
             zh["location"],
             it['html'],
             it["location"]]
        )

    if idx%500000 == 499999:
        # 一个json结束后进行排序
        all_results, all_bleu, min_score = randomFinding.save_to_csv(all_results, return_min=True)
        end_time = time.time()
        print("当前bleu为:",all_bleu, "    最小阈值为:",min_score, "    时间:{}s".format(end_time-start_time))
        start_time = time.time()
        idx = 0

    if idx%50000 == 49999:
        print("迭代次数：",idx)
    idx += 1

