from django.db import models

from articles.models import Article


class Tag(models.Model):
    """
    게시물에 태그를 추가하고 태그로 검색하는 기능을 위한 모델
    """
    hashtag = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='태그명'
    )
    article = models.ManyToManyField(
        Article,
        related_name='tags',
        verbose_name='게시물'
    )
