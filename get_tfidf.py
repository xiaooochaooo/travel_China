import math
import numpy as np
import jieba
import jieba.posseg as psg
from gensim import corpora, models
from jieba import analyse
import functools


# 停用词加载
def get_stopword_list():
    # 停用词表存储路径，每一行为一个词，按行读取进行加载
    stop_word_path = 'stop_words.utf8'
    # 进行编码转换确保匹配准确率
    stopword_list = [sw.replace('\n', '') for sw in open(stop_word_path, encoding='utf-8').readlines()]
    return stopword_list


# 定义分词函数
# 分词方法，调用jieba接口,通过pos参数确定是否采用词性标注的分词方法
def seg_to_list(sentence, pos=False):
    if not pos:
        # 不进行词性标注的分词方法
        seg_list = jieba.cut(sentence)
    else:
        # 进行词性标注的分词方法
        seg_list = psg.cut(sentence)
    return seg_list


# 步骤4：定义去除干扰词函数
# 去除干扰词
def word_filter(seg_list, pos=False):
    stopword_list = get_stopword_list()
    filter_list = []
    # 根据pos参数选择是否进行词性标注
    # 不进行词性过滤，则将词性都标注为n,表示全部保留
    for seg in seg_list:
        if not pos:
            word = seg
            flag = 'n'
        else:
            word = seg.word
            flag = seg.flag
        if not flag.startswith('n'):
            continue
        # 过滤停用词表中的词，以及长度小于2的词
        if word not in stopword_list and len(word) > 1:
            filter_list.append(word)
    return filter_list


# 定义数据加载函数
def load_data(corpus_path, pos=False):
    doc_list = []
    for line in open(corpus_path, 'r', encoding='utf-8'):
        content = line.strip()
        seg_list = seg_to_list(content, pos)
        filter_list = word_filter(seg_list, pos)
        doc_list.append(filter_list)
    return doc_list


# 定义IDF值
def train_idf(doc_list):
    idf_dic = {}
    tt_count = len(doc_list)  # 总文档数
    for doc in doc_list:
        # 计算每个词数显的文档数
        for word in set(doc):
            idf_dic[word] = idf_dic.get(word, 0) + 1.0
    for k, v in idf_dic.items():
        idf_dic[k] = math.log(tt_count / (1 + v))
    default_idf = math.log(tt_count / 1.0)
    return idf_dic, default_idf


def cmp(e1, e2):
    res = np.sign(e1[1] - e2[1])
    if res != 0:
        return res
    else:
        a = e1[0] + e2[0]
        b = e2[0] + e1[0]
        if a > b:
            return 1
        elif a == b:
            return 0
        else:
            return -1


class Tfidf:
    def __init__(self, idf_dic, default_idf, word_list, keyword_num):
        self.word_list = word_list
        self.idf_dic = idf_dic
        self.default_idf = default_idf
        self.keyword_num = keyword_num
        self.tf_dic = self.get_tf_dic()

    def get_tf_dic(self):
        tf_dic = {}
        # 词数
        for word in self.word_list:
            tf_dic[word] = tf_dic.get(word, 0) + 1
        # 计算总词数
        tt_sum = len(self.word_list)
        # v->tf值
        for k, v in tf_dic.items():
            tf_dic[k] = v / tt_sum
        return tf_dic

    def get_tfidf(self):
        tfidf_dic = {}
        for word in self.word_list:
            idf = self.idf_dic.get(word, self.default_idf)
            tf = self.tf_dic.get(word, 0)
            tfidf_dic[word] = tf * idf
        # 排序
        # lambda x:x[1]
        return sorted(tfidf_dic.items(), key=functools.cmp_to_key(cmp), reverse=True)[:self.keyword_num]


def tfidf_extract(path, work_list, pos=False, keyword_num=30):
    doc_list = load_data(path, pos)
    idf_dic, default_idf = train_idf(doc_list)
    tfidf_model = Tfidf(idf_dic, default_idf, work_list, keyword_num)
    return tfidf_model.get_tfidf()


def get_res(path):
    pos = True
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    seg_list = seg_to_list(text, pos)
    filter_list = word_filter(seg_list, pos)
    return tfidf_extract(path, filter_list)


