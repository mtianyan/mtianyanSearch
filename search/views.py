import pickle
from django.shortcuts import render
import json

from django.utils.datastructures import OrderedSet
from django.views.generic.base import View

from FunPySearch.settings.local import ES_HOST, REDIS_HOST, REDIS_PASSWORD
from search.models import ZhiHuQuestionIndex
from django.http import HttpResponse
from datetime import datetime
import redis
from elasticsearch import Elasticsearch
from django.views.generic.base import RedirectView

client = Elasticsearch(hosts=[ES_HOST])
# 使用redis实现top-n排行榜
redis_cli = redis.Redis(host=REDIS_HOST, password=REDIS_PASSWORD)


class IndexView(View):
    """首页get请求top-n排行榜"""

    @staticmethod
    def get(request):
        topn_search_clean = []
        topn_search = redis_cli.zrevrangebyscore(
            "search_keywords_set", "+inf", "-inf", start=0, num=5)
        for topn_key in topn_search:
            topn_key = str(topn_key, encoding="utf-8")
            topn_search_clean.append(topn_key)
        topn_search = topn_search_clean
        return render(request, "index.html", {"topn_search": topn_search})


class SearchSuggest(View):
    """搜索建议"""

    @staticmethod
    def get(request):
        key_words = request.GET.get('s', '')
        current_type = request.GET.get('s_type', '')
        if current_type == "question":
            return_suggest_list = []
            if key_words:
                s_question = ZhiHuQuestionIndex.search()

                """fuzzy模糊搜索, fuzziness 编辑距离, prefix_length前面不变化的前缀长度"""
                s_question = s_question.suggest('my_suggest', key_words, completion={
                    "field": "suggest", "fuzzy": {
                        "fuzziness": 2
                    },
                    "size": 10
                })
                suggestions_question = s_question.execute()
                for match in suggestions_question.suggest.my_suggest[0].options[:10]:
                    source = match._source
                    return_suggest_list.append(source["title"])
            return HttpResponse(
                json.dumps(return_suggest_list),
                content_type="application/json")


class SearchView(View):

    def get(self, request):
        key_words = request.GET.get("q", "")

        # 通用部分
        # 实现搜索关键词keyword加1操作
        redis_cli.zincrby("search_keywords_set", 1, key_words)
        # 获取topn个搜索词
        topn_search_clean = []
        topn_search = redis_cli.zrevrangebyscore(
            "search_keywords_set", "+inf", "-inf", start=0, num=5)
        for topn_key in topn_search:
            topn_key = str(topn_key, encoding="utf-8")
            topn_search_clean.append(topn_key)
        topn_search = topn_search_clean
        # 获取伯乐在线的文章数量

        jobbole_count = redis_cli.get("jobbole_blog_count")
        if jobbole_count:
            jobbole_count = pickle.loads(jobbole_count)
        else:
            jobbole_count = 0
        job_count = redis_cli.get("lagou_job_count")
        if job_count:
            job_count = pickle.loads(job_count)
        else:
            job_count = 0
        zhihu_question_count = redis_cli.get("zhihu_question_count")
        zhihu_answer_count = redis_cli.get("zhihu_answer_count")
        if zhihu_question_count:
            zhihu_question_count = pickle.loads(zhihu_question_count)
        else:
            zhihu_question_count = 0
        if zhihu_answer_count:
            zhihu_answer_count = pickle.loads(zhihu_answer_count)
        else:
            zhihu_answer_count = 0
        zhihu_count = zhihu_answer_count + zhihu_question_count

        # 当前要获取第几页的数据
        page = request.GET.get("p", "1")
        try:
            page = int(page)
        except BaseException:
            page = 1
        response = []
        start_time = datetime.now()
        s_type = request.GET.get("s_type", "")
        if s_type == "article":
            response = client.search(
                index="jobbole_blog",
                request_timeout=60,
                body={
                    "query": {
                        "multi_match": {
                            "query": key_words,
                            "fields": ["tags", "title", "content"]
                        }
                    },
                    "from": (page - 1) * 10,
                    "size": 10,
                    "highlight": {
                        "pre_tags": ['<span class="keyWord">'],
                        "post_tags": ['</span>'],
                        "fields": {
                            "title": {},
                            "content": {},
                        }
                    }
                }
            )
        elif s_type == "job":
            response = client.search(
                index="lagou_job",
                request_timeout=60,
                body={
                    "query": {
                        "multi_match": {
                            "query": key_words,
                            "fields": [
                                "title",
                                "tags",
                                "job_desc",
                                "job_advantage",
                                "company_name",
                                "job_addr",
                                "job_city",
                                "degree_need"]}},
                    "from": (
                        page - 1) * 10,
                    "size": 10,
                    "highlight": {
                        "pre_tags": ['<span class="keyWord">'],
                        "post_tags": ['</span>'],
                        "fields": {
                            "title": {},
                            "job_desc": {},
                            "company_name": {},
                        }}})
        elif s_type == "question":
            response_dict = {"question": client.search(
                index="zhihu_question",
                request_timeout=60,
                body={
                    "query": {
                        "multi_match": {
                            "query": key_words,
                            "fields": [
                                "title",
                                "content",
                                "topics"]}},
                    "from": (page - 1) * 10,
                    "size": 10,
                    "highlight": {
                        "pre_tags": ['<span class="keyWord">'],
                        "post_tags": ['</span>'],
                        "fields": {
                            "title": {},
                            "content": {},
                            "topics": {},
                        }}}), "answer": client.search(
                index="zhihu_answer",
                request_timeout=60,
                body={
                    "query": {
                        "multi_match": {
                            "query": key_words,
                            "fields": [
                                "content",
                                "author_name"]}},
                    "from": (
                        page - 1) * 10,
                    "size": 10,
                    "highlight": {
                        "pre_tags": ['<span class="keyWord">'],
                        "post_tags": ['</span>'],
                        "fields": {
                            "content": {},
                            "author_name": {},
                        }}})}

        end_time = datetime.now()
        last_seconds = (end_time - start_time).total_seconds()

        # 伯乐在线具体的信息
        hit_list = []
        error_nums = 0
        if s_type == "article":
            for hit in response["hits"]["hits"]:
                hit_dict = {}
                try:
                    if "title" in hit["highlight"]:
                        hit_dict["title"] = "".join(hit["highlight"]["title"])
                    else:
                        hit_dict["title"] = hit["_source"]["title"]
                    if "content" in hit["highlight"]:
                        hit_dict["content"] = "".join(
                            hit["highlight"]["content"])
                    else:
                        hit_dict["content"] = hit["_source"]["content"][:200]
                    hit_dict["create_date"] = hit["_source"]["create_date"]
                    hit_dict["url"] = hit["_source"]["url"]
                    hit_dict["score"] = hit["_score"]
                    hit_dict["source_site"] = "伯乐在线"
                    hit_list.append(hit_dict)
                except:
                    error_nums = error_nums + 1
        elif s_type == "job":
            for hit in response["hits"]["hits"]:
                hit_dict = {}
                try:
                    if "title" in hit["highlight"]:
                        hit_dict["title"] = "".join(hit["highlight"]["title"])
                    else:
                        hit_dict["title"] = hit["_source"]["title"]
                    if "job_desc" in hit["highlight"]:
                        hit_dict["content"] = "".join(
                            hit["highlight"]["job_desc"][:150])
                    else:
                        hit_dict["content"] = hit["_source"]["job_desc"][:150]
                    hit_dict["create_date"] = hit["_source"]["publish_time"]
                    hit_dict["url"] = hit["_source"]["url"]
                    hit_dict["score"] = hit["_score"]
                    hit_dict["company_name"] = hit["_source"]["company_name"]
                    hit_dict["source_site"] = "拉勾网"
                    hit_list.append(hit_dict)
                except:
                    hit_dict["title"] = hit["_source"]["title"]
                    hit_dict["content"] = hit["_source"]["job_desc"]
                    hit_dict["create_date"] = hit["_source"]["publish_time"]
                    hit_dict["url"] = hit["_source"]["url"]
                    hit_dict["score"] = hit["_score"]
                    hit_dict["company_name"] = hit["_source"]["company_name"]
                    hit_dict["source_site"] = "拉勾网"
                    hit_list.append(hit_dict)
        elif s_type == "question":
            for hit in response_dict["question"]["hits"]["hits"]:
                """问题"""
                hit_dict_question = {}
                if "title" in hit["highlight"]:
                    hit_dict_question["title"] = "".join(hit["highlight"]["title"])
                else:
                    hit_dict_question["title"] = hit["_source"]["title"]
                if "content" in hit["highlight"]:
                    hit_dict_question["content"] = "".join(hit["highlight"]["content"])
                else:
                    hit_dict_question["content"] = hit["_source"]["content"]
                hit_dict_question["create_date"] = hit["_source"]["crawl_time"]
                hit_dict_question["url"] = hit["_source"]["url"]
                hit_dict_question["score"] = hit["_score"]
                hit_dict_question["source_site"] = "知乎问题"
                hit_list.append(hit_dict_question)
            for hit in response_dict["answer"]["hits"]["hits"]:
                hit_dict_answer = {}
                if "author_name" in hit["highlight"]:
                    hit_dict_answer["title"] = "".join(hit["highlight"]["author_name"])
                else:
                    hit_dict_answer["title"] = hit["_source"]["author_name"]
                if "content" in hit["highlight"]:
                    hit_dict_answer["content"] = "".join(hit["highlight"]["content"])
                else:
                    hit_dict_answer["content"] = hit["_source"]["content"]
                hit_dict_answer["create_date"] = hit["_source"]["update_time"]
                hit_dict_answer["score"] = hit["_score"]
                hit_dict_answer["url"] = hit["_source"]["url"]
                hit_dict_answer["source_site"] = "知乎回答"
                hit_list.append(hit_dict_answer)
            response_dict["question"]["hits"]["total"]["value"] = response_dict["question"]["hits"]["total"]["value"] + \
                response_dict["answer"]["hits"]["total"]["value"]
            response = response_dict["question"]
        total_nums = int(response["hits"]["total"]["value"])

        # 计算出总页数
        if (page % 10) > 0:
            page_nums = int(total_nums / 10) + 1
        else:
            page_nums = int(total_nums / 10)
        return render(request, "result.html", {"page": page,
                                               "all_hits": hit_list,
                                               "key_words": key_words,
                                               "total_nums": total_nums,
                                               "page_nums": page_nums,
                                               "last_seconds": last_seconds,
                                               "topn_search": topn_search,
                                               "jobbole_count": jobbole_count,
                                               "s_type": s_type,
                                               "job_count": job_count,
                                               "zhihu_count": zhihu_count,
                                               })


favicon_view = RedirectView.as_view(
    url='http://searchstatic.mtianyan.cn/favicon.ico', permanent=True)
