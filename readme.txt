1.generate_text_data    数据预处理，这块整理的有点乱，因为时间太久了。最后的清洗结果在0_data/last_data下。
2.text_matching           核心工作，分为baseline和optim。baseline可靠稳定，但耗时长，optim耗时短，需要对结果进行二次转换。该步骤产生的最后结果整合到了baseline/file/bleu_submission下。
3.fine_tune               对上一步产生的结果进行再一次的调整，结果存在了file/bleu_after_optim下。
4.remove_bad_words        finetune后的结果存在简写的一些问题，这个文件夹负责将一些简写词去掉。结果为file/bleu_acronym。另外一个移动窗口的trick可以小幅度的提升分数。
5.result_argumented       由于之前计算bleu都是把意大利变为中文计算的，这和最终的计算方式不符合，因此不能过于相信之前的bleu结果。因此我们进行了word by word的回译，将两个bleu进行加权得到最后的得分。

注：代码能力太菜了，望谅解。