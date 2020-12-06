import mytools,os
from tqdm import tqdm

root = "../../data/processedData/zh/"
for file in tqdm(os.listdir(root)):
    ctxs = mytools.load_from_txt(root+file)

    new_ctxs = []
    for ctx in ctxs:
        # print("-----------------------------------------")
        # print(ctx)
        try:
            html, location, texts = ctx.replace("\n","").split(" | ")
        except:
            continue

        start,end = int(location.split(":")[0]),int(location.split(":")[1])

        while len(texts) > 11:
            new_texts = texts[:11]
            new_ctxs.append(
                html + " | " + str(start)+":"+str(start+11) + " | " +new_texts + "\n"
            )
            # print(html + " | " + str(start)+":"+str(start+11) + " | " +new_texts)
            texts = texts[7:]

            start = start + 7
        new_ctxs.append(html + " | " + str(start)+":"+str(end) + " | " + texts + "\n")
        # print(html + " | " + str(start)+":"+str(end) + " | " + texts)
    # exit(0)
    mytools.log_to_txt(new_ctxs, root.replace("zh","optim_zh/")+file)
    new_ctxs = []
