from dateutil.relativedelta import relativedelta
from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone

from freezegun import freeze_time

from ..models import (
    RecommendToday,
    RecommendWeekly,
    RecommendMonthly
)
from likes.models import Like
from articles.models import Article
from accounts.models import UserProfile
from commons.test import (
    get_profiles,
    get_articles,
    FROZEN_TIME,
    FROZEN_TIME_WEEK_AGO,
    FROZEN_TIME_MONTH_AGO
)


class RecommendTestCase(TestCase):
    def setUp(self):
        # month ago

        self.freezer = freeze_time(FROZEN_TIME_MONTH_AGO)
        self.freezer.start()
        self.profiles = get_profiles(30)
        self.articles_month_ago = get_articles(self.profiles[0], 30)
        for i in range(30):
            profile = self.profiles[i]
            for j in range(i+1):
                Like.objects.create(
                    profile=profile,
                    article=self.articles_month_ago[j]
                )
        self.freezer.stop()

        # week ago

        self.freezer = freeze_time(FROZEN_TIME_WEEK_AGO)
        self.freezer.start()
        self.articles_week_ago = get_articles(self.profiles[1], 30)
        for i in range(30):
            profile = self.profiles[i]
            for j in range(i+1):
                Like.objects.create(
                    profile=profile,
                    article=self.articles_week_ago[j]
                )
        self.freezer.stop()

    @freeze_time(FROZEN_TIME_MONTH_AGO)
    def test_recommend_today(self):
        queryset = RecommendToday.objects.values('recommendation').filter(created__lte=timezone.now()).order_by('-recommendation')
        for i in range(30 - 1):
            self.assertGreaterEqual(queryset[i]['recommendation'], queryset[i+1]['recommendation'])

    @freeze_time(FROZEN_TIME_WEEK_AGO)
    def test_recommend_weekly(self):
        queryset = RecommendWeekly.objects.values('recommendation').all().order_by('-recommendation')
        for i in range(30 - 1):
            self.assertGreaterEqual(queryset[i]['recommendation'], queryset[i+1]['recommendation'])

    @freeze_time(FROZEN_TIME_WEEK_AGO)
    def test_recommend_monthly(self):
        queryset = RecommendMonthly.objects.values('recommendation').all().order_by('-recommendation')
        for i in range(60 - 1):
            self.assertGreaterEqual(queryset[i]['recommendation'], queryset[i+1]['recommendation'])

