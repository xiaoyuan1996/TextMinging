import mytools
import os

ctxs = mytools.load_from_txt("all_it_vocab.txt")

remove_words = "0123456789,./;'[]\\-=<>?:\"{}|~!@#$%^&*()_+"
smooth = []
for ctx in ctxs:
    try:
        word, freq = ctx.replace("\n", "").split(" | ")

        flag = True
        for tmp in word:
            if tmp in remove_words:
                flag = False
                break
        if len(word) > 18:
            flag = False

        if flag:
            smooth.append(word+" | "+freq+"\n")
    except:
        print("error")
mytools.log_to_txt(smooth, "smooth_it_vocab.txt")