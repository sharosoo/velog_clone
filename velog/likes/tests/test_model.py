from dateutil.relativedelta import relativedelta
from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone

from freezegun import freeze_time

from ..models import Like
from articles.models import Article
from accounts.models import UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()

FROZEN_TIME_BASE = timezone.now()
FROZEN_TIME = FROZEN_TIME_BASE.strftime("%Y%m%dT%H:%M:%S")
FROZEN_TIME_WEEK_AGO = (FROZEN_TIME_BASE + relativedelta(weeks=-1)).strftime("%Y%m%dT%H:%M:%S")
FROZEN_TIME_MONTH_AGO = (FROZEN_TIME_BASE + relativedelta(months=-1)).strftime("%Y%m%dT%H:%M:%S")


class LikeTestCase(TestCase):
    def setUp(self):
        # month ago
        self.freezer = freeze_time(FROZEN_TIME_MONTH_AGO)
        self.freezer.start()

        self.user_month = User.objects.create(username='month')
        self.profile_month = UserProfile.objects.create(
            nickname='month',
            user=self.user_month,
            desc='month'
        )

        self.article = Article.objects.create(
            profile=self.profile_month,
            title='test',
            slug='test',
            content='test'
        )
        self.like_month = Like.objects.create(
            profile=self.profile_month,
            article=self.article
        )
        self.freezer.stop()

        # week ago
        self.freezer = freeze_time(FROZEN_TIME_WEEK_AGO)
        self.freezer.start()
        self.user_week = User.objects.create(username='week')
        self.profile_week = UserProfile.objects.create(
            nickname='week',
            user=self.user_week,
            desc='week'
        )
        self.like_week = Like.objects.create(
            profile=self.profile_week,
            article=self.article
        )
        self.freezer.stop()

        # today
        self.freezer = freeze_time(FROZEN_TIME)
        self.freezer.start()
        self.user_today = User.objects.create(username='today')
        self.profile_today = UserProfile.objects.create(
            nickname='today',
            user=self.user_today,
            desc='today'
        )
        self.like_today = Like.objects.create(
            profile=self.profile_today,
            article=self.article
        )

    def test_like_잘_생성됨(self):
        self.assertEqual(self.like_today.profile, self.profile_today)
        self.assertEqual(self.like_today.article, self.article)

    def test_like_unique_constraint(self):
        with self.assertRaises(IntegrityError, msg='UNIQUE constraint failed'):
            Like.objects.create(profile=self.profile_today, article=self.article)

    def test_like_period_query(self):
        self.assertEqual(Like.period.today_cnt(article_id=self.article), 1)
        self.assertEqual(Like.period.weekly_cnt(article_id=self.article), 2)
        self.assertEqual(Like.period.monthly_cnt(article_id=self.article), 3)

    def tearDown(self):
        self.freezer.stop()
