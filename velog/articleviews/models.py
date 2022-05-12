from datetime import timedelta

from dateutil.relativedelta import relativedelta
from django.db import models
from django.db.models import Q, F
from django.utils import timezone

from django_extensions.db.models import TimeStampedModel


# Todo: DRY 원칙에 위배됨 like의 PeriodQuerySet과 함께 쓸 수 있도록 리팩토링하자.
class PeriodQuerySet(models.QuerySet):

    def _period_base(self, article_id=None, time_delta=None):
        if not time_delta:
            time_delta = timedelta(0)

        time_now = timezone.now()
        period = time_now - time_delta

        if not article_id:
            return self.none()

        return self.filter(
            Q(article=article_id) &
            Q(created__gte=period)
        )

    def today(self, article_id=None):

        return self._period_base(
            article_id=article_id,
            time_delta=relativedelta(days=1)
        )

    def weekly(self, article_id=None):

        return self._period_base(
            article_id=article_id,
            time_delta=relativedelta(weeks=1)
        )

    def monthly(self, article_id=None):

        return self._period_base(
            article_id=article_id,
            time_delta=relativedelta(months=1)
        )


class ArticleViewCount(TimeStampedModel):
    article = models.ForeignKey(
        'articles.Article',
        on_delete=models.CASCADE,
        related_name='articleview',
        verbose_name='게시물조회내역'
    )

    objects = models.Manager()
    period = PeriodQuerySet.as_manager()

    class Meta:
        # ArticleViewCount 모델을 검색할때 기간에 따른 article의 조회수를 자주 검색하게 되므로 따로 index를 만들어두자.
        indexes = [
            models.Index(
                fields=['article', 'created'], name='article_period_view_idx'
            ),
        ]

    def save(self, **kwargs):
        self.article.view_cnt = F('view_cnt') + 1
        self.article.save()

        self.article.refresh_from_db()

        super(ArticleViewCount, self).save(**kwargs)
