import mytools

ctxs = mytools.load_from_txt("goodwords_dict.txt")

remove_ = "|»,# ?."

for ctx in ctxs:
    try:
        zh_, it_ = ctx.replace("\n","").split(" | ")
    except:
        items = ctx.replace("\n","").split(" | ")
        zh_, it_ = items[0], items[1]

    it_ = it_.lower()
    for i in remove_:
        it_ = it_.replace(i,"")
    mytools.log_to_txt(zh_+" | "+it_+"\n", "new_dict_lower_.txt" )
