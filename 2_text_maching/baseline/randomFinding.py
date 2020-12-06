import random
import mytools
import os,time
import pandas as pd
import numpy as np
import sys
sys.path.append("..")
# import data.dataProcess.vocab.readDict as Dict
# from data.standTest.utilize.utilize import getBleu
# import opencc
# cc = opencc.OpenCC('t2s')

def randomGetSource():
    root_source = "../data/processData/zh/"
    source_dir = root_source + random.choice(os.listdir(root_source))+"/"
    source_file = source_dir + random.choice(os.listdir(source_dir))
    source_ctx = mytools.load_from_txt(source_file)

    try:
        itemPath, start2end, text = source_ctx[random.randint(0,len(source_ctx))].split(" | ")
        itemPath = itemPath.replace("../sourceData/","")
        return itemPath, start2end, text
    except:
        return None,None,None

def randomGetTarget():
    root_source = "../data/processData/it/"
    source_dir = root_source + random.choice(os.listdir(root_source))+"/"
    source_file = source_dir + random.choice(os.listdir(source_dir))
    source_ctx = mytools.load_from_txt(source_file)

    try:
        itemPath, start2end, text = source_ctx[random.randint(0,len(source_ctx))].split(" | ")
        itemPath = itemPath.replace("../sourceData/","")
        return itemPath, start2end, text
    except:
        return None,None,None

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

def getSavedCsv():
    data = np.array(pd.read_csv("file/bleu_submission.csv"))
    return data.tolist()

def getAllRandomData(dict):
    # random_results = []
    random_results = getSavedCsv()
    all_bleu = 0
    for i in range(50000):
        print("第{}次计算，目前优化的整体bleu为{}".format(i,all_bleu))
        source_path ,source_start_end, source_text = randomGetSource()
        target_path ,target_start_end, target_text = randomGetTarget()

        if (target_text!=None) and (source_text!=None):
            # 强行翻译
            source_text = cc.convert(source_text)
            source_text = Dict.querySentence(dict, source_text)
            # 计算两者bleu分数
            bleu_score = getBleu(source_text, target_text)
            # print(bleu_score)
            # if bleu_score>0.31:
            #     print(source_text)
            #     print(target_text)
            #     print("----")

            if bleu_score >0.01:
                if [bleu_score,source_path,source_start_end,target_path,target_start_end] not in random_results:
                    random_results.append([bleu_score,
                                           source_path,
                                           source_start_end,
                                           target_path,
                                           target_start_end])

        # 每逢2000就保存一下csv
        if i % 2000 == 1999:
            random_results,all_bleu = save_to_csv(random_results)

    return random_results

