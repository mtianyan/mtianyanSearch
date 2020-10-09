import pickle

from django.contrib.auth import get_user_model
from django.shortcuts import render
import json

from FunPySearch.settings.local import ES_HOST, REDIS_HOST, REDIS_PASSWORD
from .tasks import gen_word2vec_save_to_mysql
from django.utils.datastructures import OrderedSet
from django.views.generic.base import View
from search.models import ZhiHuQuestionIndex, ZhiHuAnswerIndex
from django.http import HttpResponse
from datetime import datetime
import redis
from elasticsearch import Elasticsearch
from django.views.generic.base import RedirectView

from user.models import KeyWord2Vec, UserProfile

User = get_user_model()
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
        if current_type == "article":
            return_suggest_list = []
            if key_words:
                s = JobboleBlogIndex.search()
                """fuzzy模糊搜索, fuzziness 编辑距离, prefix_length前面不变化的前缀长度"""
                s = s.suggest('my_suggest', key_words, completion={
                    "field": "suggest", "fuzzy": {
                        "fuzziness": 2
                    },
                    "size": 10
                })
                suggestions = s.execute()
                for match in suggestions.suggest.my_suggest[0].options[:10]:
                    source = match._source
                    return_suggest_list.append(source["title"])
            return HttpResponse(
                json.dumps(return_suggest_list),
                content_type="application/json")
        elif current_type == "job":
            return_suggest_list = []
            if key_words:
                s = LagouJobIndex.search()
                s = s.suggest('my_suggest', key_words, completion={
                    "field": "suggest", "fuzzy": {
                        "fuzziness": 2
                    },
                    "size": 10
                })
                suggestions = s.execute()
                # 对于不同公司同名职位去重，提高用户体验
                name_set = OrderedSet()
                for match in suggestions.suggest.my_suggest[0].options[:10]:
                    source = match._source
                    name_set.add(source["title"])
                for name in name_set:
                    return_suggest_list.append(name)
            return HttpResponse(
                json.dumps(return_suggest_list),
                content_type="application/json")
        elif current_type == "question":
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
        try:
            gen_word2vec_save_to_mysql.delay("small", key_words)
        except:
            print("异步添加word2vec失败,检查是否开启celery: celery -A ContentSearch worker -l debug")
        try:
            history_text = request.user.history
            history_list = history_text.split(",")
            upper_score_list = []
            for history_one in history_list:
                try:
                    upper_score_list.append(history_one)
                    try:
                        key_words_vec_text = KeyWord2Vec.objects.get(keyword=history_one).keyword_word2vec
                        key_words_vec_list = key_words_vec_text.split(",")
                        for key_words_one in key_words_vec_list:
                            upper_score_list.append(key_words_one)
                    except:
                        pass
                except:
                    pass
            upper_score_set = set(upper_score_list)
            upper_score_set_list = list(upper_score_set)
            upper_score_set_list = [x for x in upper_score_set_list if x != '']
            # upper score set 涨分列表
            print(upper_score_set_list)
            history_list.append(key_words)
            history_new_set = set(history_list)
            history_new_set_list = list(history_new_set)
            history_new_txt = ",".join(history_new_set_list)
            user = UserProfile.objects.get(id=request.user.id)
            user.history = history_new_txt
            user.save()
        except:
            history_new_set_list = []
            upper_score_set_list = []
        print("*********"*30)
        history_new_set_list = [one for one in history_new_set_list if one.strip()]
        upper_score_set_list = [one for one in upper_score_set_list if one.strip()]
        print("*********"*30)
        # 通用部分
        # 实现搜索关键词keyword加1操作
        print(key_words)
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
                        "function_score": {
                            "query": {
                                "multi_match": {
                                    "query": key_words,
                                    "fields": ["title", "content"]
                                },
                            },
                            "script_score": {

                                "script": {
                                    "params": {
                                        "title_keyword": upper_score_set_list
                                    },
                                    "source": "double final_score=_score;int count=0;int total = params.title_keyword.size();while(count < total) { String upper_score_title = params.title_keyword[count]; if(doc['title_keyword'].value.contains(upper_score_title)){final_score = final_score+_score;}count++;}return final_score;"
                                }
                            }
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
        elif s_type == "question":
            body = {
                "query": {
                    "function_score": {
                        "query": {
                            "multi_match": {
                                "query": key_words,
                                "fields": ["title", "content"]
                            },
                        },
                        "script_score": {

                            "script": {
                                "params": {
                                    "title_keyword": upper_score_set_list
                                },
                                "source": "double final_score=_score;int count=0;int total = params.title_keyword.size();while(count < total) { String upper_score_title = params.title_keyword[count]; if(doc['title_keyword'].value.contains(upper_score_title)){final_score = final_score+_score;}count++;}return final_score;"
                            }
                        }
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
                        "topics": {},
                    }}}
            print(json.dumps(body,ensure_ascii=False))
            response_dict = {"question": client.search(
                index="zhihu_question",
                request_timeout=60,
                body={
                    "query": {
                        "function_score": {
                            "query": {
                                "multi_match": {
                                    "query": key_words,
                                    "fields": ["title", "content"]
                                },
                            },
                            "script_score": {

                                "script": {
                                    "params": {
                                        "title_keyword": upper_score_set_list
                                    },
                                    "source": "double final_score=_score;int count=0;int total = params.title_keyword.size();while(count < total) { String upper_score_title = params.title_keyword[count]; if(doc['title_keyword'].value.contains(upper_score_title)){final_score = final_score+_score;}count++;}return final_score;"
                                }
                            }
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
                            "topics": {},
                        }}}),

                "answer": client.search(
                    index="zhihu_answer",
                    request_timeout=60,
                    body={
                        "query": {
                            "function_score": {
                                "query": {
                                    "multi_match": {
                                        "query": key_words,
                                        "fields": ["author_name", "content"]
                                    },
                                },
                                "script_score": {

                                    "script": {
                                        "params": {
                                            "title_keyword": upper_score_set_list
                                        },
                                        "source": "double final_score=_score;int count=0;int total = params.title_keyword.size();while(count < total) { String upper_score_title = params.title_keyword[count]; if(doc['author_name'].value.contains(upper_score_title)){final_score = final_score+_score;}count++;}return final_score;"
                                    }
                                }
                            }
                        },
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
                                               "history_list": history_new_set_list,
                                               })


favicon_view = RedirectView.as_view(
    url='http://searchstatic.mtianyan.cn/favicon.ico', permanent=True)
