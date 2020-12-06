# -*- coding=utf-8 -*-
import os
import torch
import torch.nn as nn


class Searching_model(nn.Module):
    def __init__(self):
        super(Searching_model, self).__init__()

    def forward(self, it_cap, zh_cap):
        zh = zh_cap.clone()
        zh_shape = it_cap.size(0)
        max_len = it_cap.size(1)
        zh_slip = zh.contiguous().view(-1)
        zh_cube = zh_slip.unsqueeze(0).unsqueeze(2).repeat(zh_shape, 1, max_len)
        it_cube = it_cap.unsqueeze(1).repeat(1, zh_cube.size(1), 1)
        tmp = torch.gt(torch.min(torch.abs(zh_cube - it_cube), dim=2).values, 0).to(torch.float32)
        tensor_list = torch.split(tmp, max_len, dim=1)
        sum_tensor_list = [torch.sum(tensor, dim=1) for tensor in tensor_list]
        result = torch.stack(sum_tensor_list)
        return result
