from django.db import models
from django_extensions.db.models import TimeStampedModel


from recommends.managers import (
    RecommendUpdateTodayManager,
    RecommendUpdateWeeklyManager,
    RecommendUpdateMonthlyManager
)


class Recommend(TimeStampedModel):
    """
    일간, 주간, 월간 게시물 추천을 위한 base model
    """

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

    class Meta:
        abstract = True
        indexes = [
            models.Index(
                fields=['-recommendation']
            )
        ]


class RecommendToday(Recommend):
    """
    일간 게시물 추천 리스트
    """

    assigned_to = RecommendUpdateTodayManager()


class RecommendWeekly(Recommend):
    """
    주간 게시물 추천 리스트
    """

    assigned_to = RecommendUpdateWeeklyManager()


class RecommendMonthly(Recommend):
    """
    월간 게시물 추천 리스트
    """

    assigned_to = RecommendUpdateMonthlyManager()
