from django.db import models
from django_extensions.db.models import TimeStampedModel


from recommends.managers import (
    RecommendUpdateTodayManager,
    RecommendUpdateWeeklyManager,
    RecommendUpdateMonthlyManager
)


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
