# Django2.2 结合Scrapy1.6.0 ELasticSearch6.8.0 打造搜索引擎网站


[![Build Status](https://travis-ci.org/mtianyan/hexoBlog-Github.svg?branch=master)](https://travis-ci.org/mtianyan/hexoBlog-Github)
[![MIT Licence](https://badges.frapsoft.com/os/mit/mit.svg?v=103)](https://opensource.org/licenses/mit-license.php)

线上演示地址: http://search.mtianyan.cn

**本仓库为搜索引擎，网站端代码，爬虫端请前往https://github.com/mtianyan/FunpySpiderSearchEngine 获取**

## 可用功能:

1. 伯乐在线，拉勾职位，知乎爬虫存入Mysql 存入ELasticSearch
2. 全文搜索(需结合网站端一起使用)，搜索建议，我的搜索记录，搜索词高亮标红，底部分页
3. Redis实现的实时爬取数据展示，热门搜索Top-n

## 如何开始使用？

安装好爬虫端所需的相关环境。

```
git clone https://github.com/mtianyan/mtianyanSearch.git
pip install -r req_search.txt
cd mtianyanSearch
# models中修改自己的es连接地址。
python manage.py runserver
```

## 致谢

[原版视频课程地址:](https://coding.imooc.com/class/92.html)

>感谢Bobby老师的这门课程，通过这门课程学到了很多很多，自己在踩坑填坑，重磅更新解决的时候，收获的不只有知识，我觉得更多是解决问题的能力。


## 关于我

有趣的Python群：619417153

**欢迎star项目！谢谢！你的关注支持是我继续分享前进的动力**

## 求打赏鼓励

很高兴我写的文章（或我的项目代码）对你有帮助，请我吃包辣条吧!

微信打赏:

![mark](http://myphoto.mtianyan.cn/blog/180302/i52eHgilfD.png?imageslim)

支付宝打赏:

![mark](http://myphoto.mtianyan.cn/blog/180302/gDlBGemI60.jpg?imageslim)
