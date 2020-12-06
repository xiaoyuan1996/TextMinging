# -*- coding=utf-8 -*-
import os
import re
import json
import torch
import config
from tqdm import tqdm
import numpy as np
from collections import Counter


def create_valid_json(cls):
    file_path = config.source_root + cls + '/sorted_{}.json'.format(cls)
    with open(file_path, 'r', encoding='utf-8') as j:
        zh = json.load(j)

    length_counter = Counter()
    valid_corpus = []
    for item in tqdm(zh):
        txt = item['text']
        length = len(txt)
        bool_det = False
        for w in txt:
            if bool(re.search(r'\d', w)):
                bool_det = True
                break
            else:
                pass

        if bool_det:
            continue
        else:
            length_counter.update([str(length)])
            if length == 10:
                valid_corpus.append(item)
            else:
                pass

    for k in length_counter.keys():
        length = int(k)
        print('length: {} num: {} rate: {}'.format(length, length_counter[k], round(length_counter[k] / len(zh), 5)))

    with open(os.path.join(config.source_root, cls + '/valid_{}.json'.format(cls)), 'w', encoding='utf-8') as j:
        json.dump(valid_corpus, j)

    print(len(valid_corpus))


def validation_text_extraction(n):
    # word frequency stochastic
    word_counter = Counter()

    with open(os.path.join(config.source_root, 'zh/valid_zh.json'), 'r', encoding='utf-8') as j:
        zh_corpus = json.load(j)
    with open(os.path.join(config.source_root, 'it/valid_it.json'), 'r', encoding='utf-8') as j:
        it_corpus = json.load(j)

    corpus = zh_corpus + it_corpus
    for item in corpus:
        txt = item['text']
        txt_split = [txt[s:s+n] for s in range(len(txt) - n + 1)]
        word_counter.update(txt_split)

    count = 1
    word_map = {'<PAD>': 0}
    for k in word_counter.keys():
        if k in word_map.keys():
            pass
        else:
            word_map[k] = count
            count += 1

    with open(os.path.join(config.source_root, '{}_gram_word_vocab.json'.format(n)), 'w') as j:
        json.dump(word_map, j)


def word_similarity_computation(n):
    with open(os.path.join(config.source_root, '{}_gram_word_vocab.json'.format(n)), 'r', encoding='utf-8') as j:
        word_map = json.load(j)

    with open(os.path.join(config.source_root, 'it/valid_it.json'), 'r', encoding='utf-8') as j:
        it_corpus = json.load(j)
    with open(os.path.join(config.source_root, 'zh/valid_zh.json'), 'r', encoding='utf-8') as j:
        zh_corpus = json.load(j)

    # do the summary
    max_len = 0
    corpus = it_corpus + zh_corpus
    for item in corpus:
        txt = item['text']
        txt_split = [txt[s:s + n] for s in range(len(txt) - n + 1)]
        length = len(txt_split)
        max_len = max(max_len, length)

    len_it_corpus = len(it_corpus)
    len_zh_corpus = len(zh_corpus)

    it_tensor = torch.zeros((len_it_corpus, max_len))
    zh_tensor = torch.zeros((len_zh_corpus, max_len))

    for i in range(len(it_corpus)):
        item = it_corpus[i]
        txt = item['text']
        txt_split = [txt[s:s+n] for s in range(len(txt) - n + 1)]
        txt_length = len(txt_split)

        sen = [int(word_map[w]) for w in txt_split] + [0] * (max_len - txt_length)
        sen_tensor = torch.LongTensor(sen)
        it_tensor[i, ...] = sen_tensor

    for i in range(len(zh_corpus)):
        item = zh_corpus[i]
        txt = item['text']
        txt_split = [txt[s:s + n] for s in range(len(txt) - n + 1)]
        txt_length = len(txt_split)

        sen = [int(word_map[w]) for w in txt_split] + [0] * (max_len - txt_length)
        sen_tensor = torch.LongTensor(sen)
        zh_tensor[i, ...] = sen_tensor

    np.save(config.source_root + 'it/{}_gram_it_tensor.npy'.format(n), it_tensor)
    np.save(config.source_root + 'zh/{}_gram_zh_tensor.npy'.format(n), zh_tensor)


if __name__ == '__main__':
    # new_sorted_it()
    for cls in ['it', 'zh']:
        create_valid_json(cls)
    for n in [1, 2, 3, 4]:
        validation_text_extraction(n)
    for n in [1, 2, 3, 4]:
        word_similarity_computation(n)

    print('hello world')
