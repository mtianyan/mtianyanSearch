from django.conf import settings
from elasticsearch_dsl import Text, Date, Keyword, Integer, Document, Completion
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import analyzer

connections.create_connection(hosts=[settings.ES_HOST])

my_analyzer = analyzer('ik_smart')


class ZhiHuQuestionIndex(Document):
    """知乎问题"""
    suggest = Completion(analyzer=my_analyzer)
    question_id = Keyword()
    topics = Text(analyzer="ik_max_word")
    url = Keyword()
    title = Text(analyzer="ik_max_word")
    title_keyword = Keyword()
    content = Text(analyzer="ik_max_word")
    answer_num = Integer()
    comments_num = Integer()
    watch_user_num = Integer()
    click_num = Integer()

    crawl_time = Date()

    class Index:
        name = 'zhihu_question'


class ZhiHuAnswerIndex(Document):
    """知乎回答"""
    suggest = Completion(analyzer=my_analyzer)

    answer_id = Keyword()
    question_id = Keyword()
    author_id = Keyword()
    author_name = Keyword()

    content = Text(analyzer="ik_smart")
    praise_num = Integer()
    comments_num = Integer()
    url = Keyword()
    create_time = Date()

    update_time = Date()
    crawl_time = Date()

    class Index:
        name = 'zhihu_answer'
