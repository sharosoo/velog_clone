from django.test import TestCase

from ..models import Series
from django.contrib.auth import get_user_model
from accounts.models import UserProfile
from articles.models import Article

User = get_user_model()


class SeriesTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='test'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            nickname='test'
        )
        self.article = Article.objects.create(
            profile=self.profile,
            title='title',
            slug='slug',
            content='content'
        )
        self.series = Series.objects.create(
            title='test',
            profile=self.profile
        )

    def test_series(self):
        self.assertTrue(Series.objects.all().exists())

    def test_series_order(self):
        self.article.series = self.series
        self.article.save()
        self.assertEqual(self.article.series_order, 1)
