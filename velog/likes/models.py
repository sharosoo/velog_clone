from datetime import timedelta

from dateutil.relativedelta import relativedelta
from django.db import models
from django.db.models import Q
from django.utils import timezone

from django_extensions.db.models import TimeStampedModel

from accounts.models import UserProfile
from articles.models import Article


class PeriodQuerySet(models.QuerySet):

    def _period_base(self, article_id=None, time_delta=None):
        if not time_delta:
            time_delta = timedelta(0)

        time_now = timezone.now()
        period = time_now - time_delta

        if not article_id:
            return self.filter(
                Q(created__gte=period)
            )

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

    # Todo: 다른 모델에서 불러오는 것이 바람직, Recommend에서 관리하자
    def today_cnt(self, article_id=None):

        return self.today(
            article_id=article_id
        ).count()

    def weekly_cnt(self, article_id=None):

        return self.weekly(
            article_id=article_id
        ).count()

    def monthly_cnt(self, article_id=None):

        return self.monthly(
            article_id=article_id
        ).count()


class Like(TimeStampedModel):
    """
    1. 정의
        user마다 각 article에 좋아요를 누를 수 있는 기능을 구현한 모델

    3. 참고
        기간별 like를 쿼리하기 위해서는 period manager를 이용할 것(today, weekly, monthly)
        좋아요 수는 today_cnt, weekly_cnt, monthly_cnt를 이용한다.
    """
    # unlike하면 어차피 DB에서 삭제할거라서 굳이 modified 필드가 필요 없기는 하다.

    profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='like'
    )

    objects = models.Manager()
    # 시기별(today, weekly, monthly)로 게시물 당 좋아요 수를 쿼리할 수 있다.
    period = PeriodQuerySet.as_manager()

    class Meta:
        # 좋아요는 각 article에 대해 user마다 한번씩만 누를 수 있다.
        constraints = [
            models.UniqueConstraint(
                fields=['profile', 'article'],
                name='unique like'
            ),
        ]
        # like 모델을 검색할때 기간에 따른 article의 좋아요 수를 자주 검색하게 되므로 따로 index를 만들어두자.
        indexes = [
            models.Index(
                fields=['article'], name='article_idx'
            ),
            models.Index(
                fields=['article', 'created'], name='article_period_like_idx'
            ),
        ]
