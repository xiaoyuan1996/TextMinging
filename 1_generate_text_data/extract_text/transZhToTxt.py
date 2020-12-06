import os
import mytools
import utilize

rootpaths = [
"../../data/zhit-0825/zh/2020-04-18/",
]

for rootpath in rootpaths:
    for idx,item in enumerate(os.listdir(rootpath)):

        try:
            with open(rootpath+item,encoding='UTF-8') as f:
                s=f.read()
            for line in s.split("\n"):
                # 分割每一行
                texts = utilize.filterForLine(line)
                if texts != []:
                    for text in texts:
                        if text != "":
                            # 计算每一个文本的起始位置和终止位置
                            start,end = utilize.calcIndexForPiece(text, s)

                            # 生成item 写入文件
                            ctx = rootpath+item+" | "+str(start)+":"+str(end)+" | "+text
                            mytools.log_to_txt(ctx,rootpath.replace("zhit-0825","processedData")+str(int(idx/1000))+rootpath.replace("/","")+".txt",encoding="UTF-8")
        except:
            pass

        print(rootpath+" Finished:{}/{}".format(idx,len(os.listdir(rootpath))))
