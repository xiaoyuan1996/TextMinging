import random
import mytools
import os,time
import pandas as pd
import numpy as np
import sys
import utils
from tqdm import tqdm
import re
pat1=re.compile(r'[\u00e0-\u00ff]+')

# 读取字典
Dict = utils.readDict(path = "utils/filter_vocab.txt")

def load_raw(html, loc):
    zh_file_name = "../0_data/zhit-0825/" + html
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
    data = np.array(pd.read_csv("file/bleu_after_optim.csv"))
    return data.tolist()

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

def read_text_from_file(route, start, end):
    with open(route, encoding='UTF-8') as f:
        source = f.read()[start:end]
    return source

def compute_column_score(item):
    """
    给定一行数据，返回至多1000行结果
    :param item:data中的一行
    :return: 相似度数组
    """
    zh_route = "../0_data/zhit-0825/"+item[0]
    ja_route = "../0_data/zhit-0825/"+item[2]

    # 读取文本所在行数
    zh_start,zh_end = int(item[1].split(":")[0]),int(item[1].split(":")[1])
    ja_start,ja_end = int(item[3].split(":")[0]),int(item[3].split(":")[1])

    # search
    searched_results = []
    zh_all = read_text_from_file(zh_route, zh_start, zh_end)
    zh_all_filter = replace_all_blank(zh_all)

    ja_all = read_text_from_file(ja_route, ja_start, ja_end)
    ja_translate = utils.querySentence(Dict, ja_all)

    score = utils.compute_item_score(ja_translate, zh_all_filter)

    if len(zh_all_filter) == 5:
        for ja_windows_lens in range(len(ja_all), 5, -1):
            for start_bias in range(ja_start, ja_end - ja_windows_lens):
                ja_tmp = ja_all[start_bias - ja_start: start_bias - ja_start + ja_windows_lens]
                ja_translate = utils.querySentence(Dict, ja_tmp)

                score = utils.compute_item_score(ja_translate, zh_all_filter)

                if score > 0.5:
                    searched_results.append([score, item[0], item[1], item[2], str(start_bias)+":"+str(start_bias+ja_windows_lens)])
        log_info = " ".join(item) + "\n"
        mytools.log_to_txt(log_info, "file/already_finished.txt")
        return searched_results

    else:
        if score > 0.5:
            searched_results.append([score, item[0], item[1], item[2], item[3]])

        for ja_windows_lens in range(len(ja_all),5, -1):
            for start_bias in range(ja_start, ja_end-ja_windows_lens):
                ja_tmp = ja_all[start_bias-ja_start: start_bias-ja_start+ja_windows_lens]
                ja_translate = utils.querySentence(Dict, ja_tmp)

                for zh_windows_lens in range(len(zh_all), 4, -1):
                    for start_bias_zh in range(zh_start, zh_end-zh_windows_lens):
                        zh_tmp = zh_all[start_bias_zh-zh_start: start_bias_zh-zh_start+zh_windows_lens]
                        zh_tmp_filter = replace_all_blank(zh_tmp)
                        if len(zh_tmp_filter) <= 4:
                            continue

                        score = utils.compute_item_score(ja_translate, zh_tmp_filter)

                        if score > 0.5:
                            searched_results.append([score, item[0], str(start_bias_zh)+":"+str(start_bias_zh+zh_windows_lens),
                                                     item[2], str(start_bias)+":"+str(start_bias+ja_windows_lens)] )
        # 记录已完成
        log_info = " ".join(item)+"\n"
        mytools.log_to_txt(log_info, "file/already_finished.txt")

        return searched_results

def main():
    # Read already finished
    already_finished = []
    if os.path.exists("file/already_finished.txt"):
        already_finished = mytools.load_from_txt("file/already_finished.txt")

    # Read data
    data = np.array(pd.read_csv("../2_text_maching/baseline/file/submission.csv"))
    data =  data.tolist()

    refine_data = []
    if os.path.exists("file/bleu_after_optim.csv"):
        refine_data = getSavedCsv()

    for idx,d in tqdm(enumerate(data)):
        if idx % 1000 == 999:
            refine_data,all_bleu = save_to_csv(refine_data, default_path = "after_optim")
            print("lens of refine_data:",len(refine_data))
            print("now bleu is: ",all_bleu )


        if " ".join(d)+"\n" in already_finished:
            continue

        tmp_data = compute_column_score(d)
        for t in tmp_data:
            refine_data.append(t)

    data = np.array(pd.read_csv("file/bleu_after_optim.csv"))
    print("After Optim:",np.sum(np.transpose(data)[0]))

if __name__=="__main__":
    main()


