import django
from gensim.models import KeyedVectors
import gensim

import sys
import os

# 获取当前文件的目录
from FunPySearch.celery import app

pwd = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
# 获取项目名的目录(因为我的当前文件是在项目名下的文件夹下的文件.所以是../)
sys.path.append(pwd)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FunPySearch.settings")
django.setup()
from user.models import KeyWord2Vec  # 必须放着


def gen_word2vec_save_to_mysql_test(model_name="small", keyword=None):
    if model_name == "small":
        model = gensim.models.Word2Vec.load("./trained_models/zhihu.model")
        word2vec_list = model.wv.most_similar(keyword, topn=5)
    elif model_name == "tencent":
        model = KeyedVectors.load_word2vec_format("./trained_models/45000-small.txt")
        word2vec_list = model.most_similar(keyword, topn=5)
    elif model_name == "zhihu":
        model = KeyedVectors.load_word2vec_format("./trained_models/sgns.zhihu.bigram-char")
        word2vec_list = model.most_similar(keyword, topn=5)
    word2vec_list_common = []
    for item in word2vec_list:
        word2vec_list_common.append(item[0])
    word2vec_text = ",".join(word2vec_list_common)
    print(word2vec_text)


@app.task
def gen_word2vec_save_to_mysql(model_name="small", keyword=None):
    if model_name == "small":
        try:
            model = gensim.models.Word2Vec.load("./search/trained_models/zhihu.model")
            word2vec_list = model.wv.most_similar(keyword, topn=5)
        except KeyError:
            word2vec_list = []
    elif model_name == "tencent":
        model = KeyedVectors.load_word2vec_format("./search/trained_models/45000-small.txt")
        word2vec_list = model.most_similar(keyword, topn=5)
    elif model_name == "zhihu":
        model = KeyedVectors.load_word2vec_format("./search/trained_models/sgns.zhihu.bigram-char")
        word2vec_list = model.most_similar(keyword, topn=5)
    word2vec_list_common = []
    for item in word2vec_list:
        word2vec_list_common.append(item[0])
    word2vec_text = ",".join(word2vec_list_common)
    print(word2vec_text)
    if KeyWord2Vec.objects.filter(keyword=keyword):
        pass
    else:
        keyword_word2vec = KeyWord2Vec()
        keyword_word2vec.keyword = keyword
        keyword_word2vec.keyword_word2vec = word2vec_text
        keyword_word2vec.save()


def test_us_small_model():
    model = gensim.models.Word2Vec.load("./trained_models/zhihu.model")
    print(model.wv.most_similar('老公', topn=8))
    print("*" * 20)


def test_tencent_ai_model():
    model = KeyedVectors.load_word2vec_format("./trained_models/45000-small.txt")
    print(model.most_similar('特朗普', topn=10))
    print("*" * 20)
    print(model.most_similar(positive=['女', '国王'], negative=['男'], topn=1))
    print("*" * 20)
    print(model.doesnt_match("上海 成都 广州 北京".split(" ")))
    print("*" * 20)
    print(model.similarity('女人', '男人'))


def test_zhihu_model():
    model = KeyedVectors.load_word2vec_format("./trained_models/sgns.zhihu.bigram-char")
    print(model.most_similar('特朗普', topn=10))
    print("*" * 20)
    print(model.most_similar(positive=['女', '国王'], negative=['男'], topn=1))
    print("*" * 20)
    print(model.doesnt_match("上海 成都 广州 北京".split(" ")))
    print("*" * 20)
    print(model.similarity('女人', '男人'))


if __name__ == '__main__':
    # print("使用我们自己训练的微型知乎wordvec模型: ")
    # test_us_small_model()
    # print("使用腾讯ai实验室word2vec模型: ")  # https://ai.tencent.com/ailab/nlp/embedding.html
    # test_tencent_ai_model()
    # print("使用中文开源知乎word2vec模型")     # https://github.com/Embedding/Chinese-Word-Vectors
    # test_zhihu_model()
    # print("************************")
    gen_word2vec_save_to_mysql_test("small", "老公")
