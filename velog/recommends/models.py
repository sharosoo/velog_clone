from django.db import models
from django_extensions.db.models import TimeStampedModel

from likes.models import Like
from articleviews.models import ArticleViewCount
from recommends.basemanager import RecommendUpdateBaseManager


class RecommendUpdateMonthlyManager(RecommendUpdateBaseManager):
    def get_article_like_cnt(self, article):
        return Like.period.monthly(article_id=article).count()

    def get_article_view_cnt(self, article):
        return ArticleViewCount.period.monthly_cnt(article_id=article).count()


class RecommendUpdateWeeklyManager(RecommendUpdateBaseManager):
    def get_article_like_cnt(self, article):
        return Like.period.weekly(article_id=article).count()

    def get_article_view_cnt(self, article):
        return ArticleViewCount.period.weekly(article_id=article).count()


class RecommendUpdateTodayManager(RecommendUpdateBaseManager):
    def get_article_like_cnt(self, article):
        return Like.period.today(article_id=article).count()

    def get_article_view_cnt(self, article):
        return ArticleViewCount.period.today(article_id=article).count()


class Recommend(TimeStampedModel):

    article = models.OneToOneField(
        'articles.Article',
        on_delete=models.CASCADE,
    )

    recommendation = models.PositiveIntegerField(
        blank=True,
        default=0,
        verbose_name='추천지수'
    )

    objects = models.Manager()
    assigned_to = RecommendUpdateBaseManager()

    def get_class_name(self):
        return self.__class__.__name__

    class Meta:
        abstract = True
        indexes = [
            models.Index(
                fields=['-recommendation']
            )
        ]


class RecommendToday(Recommend):

    assigned_to = RecommendUpdateTodayManager()


class RecommendWeekly(Recommend):

    assigned_to = RecommendUpdateWeeklyManager()


class RecommendMonthly(Recommend):

    assigned_to = RecommendUpdateMonthlyManager()