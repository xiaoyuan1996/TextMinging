import os,sys
from ots_python3_demo.ots_python3_demo import WebOTS
import time
import mytools

host = "ntrans.xfyun.cn"
# 初始化类
gClass = WebOTS.get_result(host)

# text = "hello world"
# respData = gClass.call_url(text=text)
# print(respData["data"]["result"]["trans_result"]['dst'])

ctxs = mytools.load_from_txt("smooth_it_vocab.txt")

i = 0
for ctx in ctxs:
    try:
        # print(ctx.replace("\n","").split(" | ")[0])
        # ans = translate(fromLang='zh', toLang='it', q=ctx.replace("\n","").split(" | ")[0])
        ans = gClass.call_url(text=ctx.replace("\n","").split(" | ")[0])["data"]["result"]["trans_result"]['dst']
        # print(ans)
        if ans == None:
            ans = "unknown"
    except:
        ans = "unknown"

    tmp = ctx.replace("\n","").split(" | ")[0] + " | " + ans + "\n"
    mytools.log_to_txt(tmp, "smooth_xunfei_dict.txt")

    i += 1

    print(i,"/",len(ctxs))
    # time.sleep(0.01)

    if i % 500 == 499:
        # 初始化类
        gClass = WebOTS.get_result(host)

