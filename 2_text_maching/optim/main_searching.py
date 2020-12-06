# -*- coding=utf-8 -*-
import os
import json
import time
import config
from data.search_dataset import new_data_set
import torch
import torch.utils.data as Data
from tqdm import tqdm
from models.Search_model import Searching_model
import numpy as np


def main():
    batch_size = config.batch_size
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    dataset = new_data_set()
    data_loader = Data.DataLoader(batch_size=batch_size,
                                  dataset=dataset,
                                  pin_memory=True)

    small_length = dataset.smaller_length()
    model = Searching_model()

    total_result_list = []

    start_time = time.time()
    for it_tuple, zh_tuple, index in tqdm(data_loader):
        index = index.squeeze(1)
        it_1, zh_1 = it_tuple[0], zh_tuple[0]
        it_2, zh_2 = it_tuple[1], zh_tuple[1]
        it_3, zh_3 = it_tuple[2], zh_tuple[2]
        it_4, zh_4 = it_tuple[3], zh_tuple[3]

        result_1 = model(it_1.to(device), zh_1.to(device))
        result_2 = model(it_2.to(device), zh_2.to(device))
        result_3 = model(it_3.to(device), zh_3.to(device))
        result_4 = model(it_4.to(device), zh_4.to(device))

        result_all = torch.floor((result_1 + result_2 + result_3 + result_4) / 4).to(torch.int64)

        result_value, index_list = torch.topk(result_all, k=1, dim=1, largest=False)
        index_copy = index_list.clone().squeeze(1)

        real_index = torch.zeros_like(index_copy)
        index_list = index_copy.tolist()
        for i in range(len(index_list)):
            value = index[index_list[i]]
            real_index[i] = value

        result_matrix = torch.cat([result_value, real_index.unsqueeze(1)], dim=1)
        total_result_list.append(result_matrix)

    end_time = time.time()
    times = end_time - start_time
    h = round(times//3600)
    m = round((times - h*3600) // 60)
    s = times - h*3600 - m*60
    print('cost times: {}h {}m {}s'.format(h, m, s))

    total_result = torch.cat(total_result_list, dim=0)
    _, f_idx = torch.topk(total_result[:, 0], k=50000, dim=0, largest=False)

    np.save(config.source_root + 'total_result.npy', total_result.cpu())

    # index summary
    exist_list = []
    for idx in f_idx:
        item = total_result[idx, ...][1].item()
        score = total_result[idx, ...][0].item()
        item = item % small_length
        if item in exist_list:
            pass
        else:
            exist_list.append((idx.item(), item, score))

    final_list = exist_list[:40000]

    with open(os.path.join(config.source_root, 'index_list.json'), 'w') as j:
        json.dump(final_list, j)


if __name__ == '__main__':
    main()

