from dateutil.relativedelta import relativedelta
from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone

from freezegun import freeze_time

from ..models import ArticleViewCount
from articles.models import Article
from accounts.models import UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()

FROZEN_TIME_BASE = timezone.now()
FROZEN_TIME = FROZEN_TIME_BASE.strftime("%Y%m%dT%H:%M:%S")
FROZEN_TIME_WEEK_AGO = (FROZEN_TIME_BASE + relativedelta(weeks=-1)).strftime("%Y%m%dT%H:%M:%S")
FROZEN_TIME_MONTH_AGO = (FROZEN_TIME_BASE + relativedelta(months=-1)).strftime("%Y%m%dT%H:%M:%S")


class ArticleViewCountTestCase(TestCase):
    def setUp(self):
        # month ago
        self.freezer = freeze_time(FROZEN_TIME_MONTH_AGO)
        self.freezer.start()

        self.user = User.objects.create(username='month')
        self.profile = UserProfile.objects.create(
            nickname='test',
            user=self.user,
            desc='test'
        )

        self.article = Article.objects.create(
            profile=self.profile,
            title='test',
            slug='test',
            content='test'
        )
        self.view_month = ArticleViewCount.objects.create(
            article=self.article
        )
        self.freezer.stop()

        # week ago
        self.freezer = freeze_time(FROZEN_TIME_WEEK_AGO)
        self.freezer.start()
        self.view_week = ArticleViewCount.objects.create(
            article=self.article
        )
        self.freezer.stop()

        # today
        self.freezer = freeze_time(FROZEN_TIME)
        self.freezer.start()

        self.view_today = ArticleViewCount.objects.create(
            article=self.article
        )

    def test_article_view_잘_생성됨(self):
        self.assertEqual(self.view_today.article, self.article)

    def test_article_view_period_query(self):
        self.assertEqual(ArticleViewCount.period.today_cnt(article_id=self.article.id), 1)
        self.assertEqual(ArticleViewCount.period.weekly_cnt(article_id=self.article.id), 2)
        self.assertEqual(ArticleViewCount.period.monthly_cnt(article_id=self.article.id), 3)

    def test_article의_view_cnt값이_올바르게_생성됨(self):
        self.assertEqual(self.article.view_cnt, 3)

    def tearDown(self):
        self.freezer.stop()
