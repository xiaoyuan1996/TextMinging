# -*- coding=utf-8 -*-
import os
import config
import torch
import torch.utils.data as Data
import numpy as np


class new_data_set(Data.Dataset):
    def __init__(self):
        self.it_tensor_1 = np.load(config.source_root + 'it/1_gram_it_tensor.npy')
        self.it_tensor_2 = np.load(config.source_root + 'it/2_gram_it_tensor.npy')
        self.it_tensor_3 = np.load(config.source_root + 'it/3_gram_it_tensor.npy')
        self.it_tensor_4 = np.load(config.source_root + 'it/4_gram_it_tensor.npy')

        self.zh_tensor_1 = np.load(config.source_root + 'zh/1_gram_zh_tensor.npy')
        self.zh_tensor_2 = np.load(config.source_root + 'zh/2_gram_zh_tensor.npy')
        self.zh_tensor_3 = np.load(config.source_root + 'zh/3_gram_zh_tensor.npy')
        self.zh_tensor_4 = np.load(config.source_root + 'zh/4_gram_zh_tensor.npy')

        self.len_it = self.it_tensor_1.shape[0]
        self.len_zh = self.zh_tensor_1.shape[0]
        self.max_len_1 = self.it_tensor_1.shape[1]
        self.max_len_2 = self.it_tensor_2.shape[1]
        self.max_len_3 = self.it_tensor_3.shape[1]
        self.max_len_4 = self.it_tensor_4.shape[1]

    def __getitem__(self, i):
        j = i % self.len_it
        j1 = i % self.len_zh
        it_t_1 = torch.from_numpy(self.it_tensor_1[j, ...]).to(torch.float32)
        it_t_2 = torch.from_numpy(self.it_tensor_2[j, ...]).to(torch.float32)
        it_t_3 = torch.from_numpy(self.it_tensor_3[j, ...]).to(torch.float32)
        it_t_4 = torch.from_numpy(self.it_tensor_4[j, ...]).to(torch.float32)

        zh_t_1 = torch.from_numpy(self.zh_tensor_1[j1, ...]).to(torch.float32)
        zh_t_2 = torch.from_numpy(self.zh_tensor_2[j1, ...]).to(torch.float32)
        zh_t_3 = torch.from_numpy(self.zh_tensor_3[j1, ...]).to(torch.float32)
        zh_t_4 = torch.from_numpy(self.zh_tensor_4[j1, ...]).to(torch.float32)

        index = torch.LongTensor([i])

        return (it_t_1, it_t_2, it_t_3, it_t_4), (zh_t_1, zh_t_2, zh_t_3, zh_t_4), index

    def __len__(self):
        return self.len_zh

    def smaller_length(self):
        return min(self.len_it, self.len_zh)
