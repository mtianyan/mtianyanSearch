from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class UserProfile(AbstractUser):
    history = models.CharField(max_length=128, verbose_name="搜索历史", default="")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class KeyWord2Vec(models.Model):
    keyword = models.CharField(max_length=128, verbose_name="搜索历史关键词", default="")
    keyword_word2vec = models.CharField(max_length=256, verbose_name="关键词word2vec", default="")

    class Meta:
        verbose_name = "关键词word2vec"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.keyword
