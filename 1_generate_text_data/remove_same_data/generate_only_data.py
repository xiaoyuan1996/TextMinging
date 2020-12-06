import mytools,os
from tqdm import tqdm

ctxs = mytools.load_from_txt("sorted_data/zh.txt")

for ctx in tqdm(ctxs):
    text, pos = ctx.split(" ||| ")
    html,location = pos.replace("\n","").split(" || ")[0].split(" | ")
    ctx = html + " | " + location + " | " + text + "\n"
    mytools.log_to_txt(ctx, "sorted_data/sorted_zh.txt")
