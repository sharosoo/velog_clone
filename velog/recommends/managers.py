from django.db import models

from likes.models import Like
from articleviews.models import ArticleViewCount


class RecommendUpdateBaseManager(models.Manager):

    def get_object_or_create(self, article):
        instances = self.filter(article=article)
        if instances.exists():
            return instances[0]

        instance = super().create(article=article)
        return instance

    def update_article_recommend(self, article):
        instance = self.get_object_or_create(article=article)

        update_value = self.get_article_like_cnt(article) * 5 \
                       + self.get_article_view_cnt(article)

        instance.recommendation = update_value
        instance.save()

    def get_article_like_cnt(self, article):
        raise NotImplementedError

    def get_article_view_cnt(self, article):
        raise NotImplementedError


class RecommendUpdateMonthlyManager(RecommendUpdateBaseManager):

    def get_article_like_cnt(self, article):
        return Like.period.monthly(article_id=article).count()

    def get_article_view_cnt(self, article):
        return ArticleViewCount.period.monthly(article_id=article).count()


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
