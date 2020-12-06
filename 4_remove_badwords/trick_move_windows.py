import pandas as pd
import numpy as np
from nltk.translate.bleu_score import sentence_bleu,SmoothingFunction,corpus_bleu
from tqdm import tqdm
# 读取字典
def load_raw(html, loc):
    zh_file_name = "../data0/zhit-0825/" + html
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

# 测试两条语句的bleu
def getBleu(source,target):
    sf7 = SmoothingFunction().method7
    r = sentence_bleu([source], target, weights=(0.25, 0.25, 0.25, 0.25), smoothing_function=sf7)
    return r

def optim_item(last_bleu, zh_file, zh_pos, ja_file, ja_pos, flag=0):

    zh_start,zh_end = zh_pos.split(":")
    zh_start, zh_end = int(zh_start),int(zh_end)

    ja_start,ja_end = ja_pos.split(":")
    ja_start, ja_end = int(ja_start),int(ja_end)

    if flag == 0:
        last_bleu -= 0.01
        return [last_bleu, zh_file, str(zh_start - 1) + ":" + str(zh_end), ja_file,
                str(ja_start) + ":" + str(ja_end+1)]

    elif flag == 1:
        last_bleu -= 0.012
        return [last_bleu, zh_file, str(zh_start) + ":" + str(zh_end+1), ja_file,
                str(ja_start-1) + ":" + str(ja_end)]

    else:
        return [last_bleu, zh_file, str(zh_start) + ":" + str(zh_end), ja_file, str(ja_start) + ":" + str(ja_end)]

def main():
    csv_path = "file/bleu_acronym.csv"
    data = np.array(pd.read_csv(csv_path))
    print("Before Optim:",np.sum(np.transpose(data[:10000])[0]))
    exit(0)
    # data = data[:10000]

    new_data = []
    for i,(last_bleu, zh_file, zh_pos, ja_file, ja_path) in tqdm(enumerate(data)):
        item = optim_item(last_bleu, zh_file, zh_pos, ja_file, ja_path, flag=0)
        new_data.append(item)
        item = optim_item(last_bleu, zh_file, zh_pos, ja_file, ja_path, flag=1)
        new_data.append(item)

        item = optim_item(last_bleu, zh_file, zh_pos, ja_file, ja_path, flag=5)
        new_data.append(item)

    save_to_csv(new_data,default_path = "submission")

    new_data = np.transpose(np.array(new_data))[0]
    new_data = np.sort(new_data)[::-1]
    sum_new_data = 0
    for d in new_data[:10000]:
        sum_new_data += float(d)
    print("After Optim:",sum_new_data)


main()


