from .base import *

try:
    var = os.environ["not_use_docker"]
    UseDocker = False
except KeyError:
    UseDocker = True
if UseDocker:
    ES_HOST = "mtianyan_elasticsearch"
    REDIS_HOST = "mtianyan_redis"
    REDIS_PASSWORD = "mtianyanRedisRoot"
else:
    ES_HOST = "localhost"
    REDIS_HOST = "localhost"
    REDIS_PASSWORD = "mtianyanRedisRoot"
