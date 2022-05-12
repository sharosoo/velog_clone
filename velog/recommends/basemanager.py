from django.db import models


class RecommendUpdateBaseManager(models.Manager):

    def get_queryset(self, article):
        return super().get_queryset().filter(
            article=article
        )

    def get_object_or_create(self, article):
        instances = self.get_queryset(article)
        if instances.exists():
            return instances[0]

        instance = super().create(article=article)
        return instance

    def update_article_recommend(self, article):
        instance = self.get_object_or_create(article)

        update_value = self.get_article_like_cnt(article) * 5 \
                       + self.get_article_view_cnt(article)

        instance.recommendation = update_value
        instance.save()

    def get_article_like_cnt(self, article):
        raise NotImplementedError

    def get_article_view_cnt(self, article):
        raise NotImplementedError
