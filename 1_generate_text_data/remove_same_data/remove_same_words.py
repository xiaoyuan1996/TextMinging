import mytools,os
from tqdm import tqdm

root_path = "../filter_data/sorted_data/zh/"
saved_results = {}
all_idx = 0
for file in tqdm(os.listdir(root_path)):
    try:
        ctxs = mytools.load_from_txt(root_path+file)

        # try:
        for ctx in ctxs:
            all_idx += 1
            html, location, text = ctx.replace("\n","").split(" | ")

            if text not in saved_results:
                saved_results[text] = [
                    html + " | " + location
                ]
            else:
                saved_results[text].append(html + " | " + location)
    except:
        pass

print(all_idx)
print(len(saved_results.keys()))

for k in tqdm(saved_results.keys()) :
    mytools.log_to_txt(k+" ||| "+" || ".join(saved_results[k])+"\n", "saved_results/zh.txt")




"""
1202420
582393

3215128
1162976
"""