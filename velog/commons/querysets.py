from datetime import timedelta

from dateutil.relativedelta import relativedelta
from django.db import models
from django.db.models import Q
from django.utils import timezone


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
