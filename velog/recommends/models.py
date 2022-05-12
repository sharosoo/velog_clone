from django.db import models
from django_extensions.db.models import TimeStampedModel

from likes.models import Like
from articleviews.models import ArticleViewCount


class Recommend(TimeStampedModel):

    article = models.ForeignKey(
        'articles.Article',
        on_delete=models.CASCADE,
    )

    recommendation = models.PositiveIntegerField(
        blank=True,
        default=0,
        verbose_name='추천지수'
    )

    class Meta:
        abstract = True

    def get_recommendation_value(self):
        raise NotImplementedError


class RecommendToday(Recommend):
    def get_recommendation_value(self):
        return self.get_view_cnt_today() + 5 * self.get_like_today()

    def get_like_today(self):
        return Like.period.today_cnt(article_id=self.article)

    def get_view_cnt_today(self):
        return ArticleViewCount.period.today_cnt(article_id=self.article)


class RecommendWeekly(Recommend):
    def get_recommendation_value(self):
        return self.get_view_cnt_weekly() + 5 * self.get_like_weekly()

    def get_like_weekly(self):
        return Like.period.weekly_cnt(article_id=self.article)

    def get_view_cnt_weekly(self):
        return ArticleViewCount.period.weekly_cnt(article_id=self.article)


class RecommendMonthly(Recommend):
    def get_recommendation_value(self):
        return self.get_view_cnt_monthly() + 5 * self.get_like_monthly()

    def get_like_monthly(self):
        return Like.period.monthly_cnt(article_id=self.article)

    def get_view_cnt_monthly(self):
        return ArticleViewCount.period.monthly_cnt(article_id=self.article)