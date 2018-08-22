from elasticsearch_dsl import Text, Date, Keyword, Integer, Document, Completion
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import analyzer

connections.create_connection(hosts=["localhost"])

my_analyzer = analyzer('ik_smart')


class JobboleBlogIndex(Document):
    """伯乐在线文章类型"""
    suggest = Completion(analyzer=my_analyzer)
    title = Text(analyzer="ik_max_word")
    create_date = Date()
    url = Keyword()
    url_object_id = Keyword()
    front_image_url = Keyword()
    praise_nums = Integer()
    comment_nums = Integer()
    fav_nums = Integer()
    tags = Text(analyzer="ik_max_word")
    content = Text(analyzer="ik_smart")

    class Index:
        name = 'jobbole_blog'


class LagouJobIndex(Document):
    """拉勾网工作职位"""
    suggest = Completion(analyzer=my_analyzer)
    title = Text(analyzer="ik_max_word")
    url = Keyword()
    url_object_id = Keyword()
    salary_min = Integer()
    salary_max = Integer()
    job_city = Keyword()
    work_years_min = Integer()
    work_years_max = Integer()
    degree_need = Text(analyzer="ik_max_word")
    job_type = Keyword()
    publish_time = Date()
    job_advantage = Text(analyzer="ik_max_word")
    job_desc = Text(analyzer="ik_smart")
    job_addr = Text(analyzer="ik_max_word")
    company_name = Keyword()
    company_url = Keyword()
    tags = Text(analyzer="ik_max_word")
    crawl_time = Date()

    class Index:
        name = 'lagou_job'


class ZhiHuQuestionIndex(Document):
    """知乎问题"""
    suggest = Completion(analyzer=my_analyzer)

    question_id = Keyword()
    topics = Text(analyzer="ik_max_word")
    url = Keyword()
    title = Text(analyzer="ik_max_word")

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
