1.首先通过utils中的工具，将大型语料库，输出有效语料库，并生成所有n-gram矩阵，
2.然后直接调用mainsearching即可，得到最相关的index：（zh_index, it_index, score）