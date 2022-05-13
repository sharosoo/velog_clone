from django.test import TestCase
from django.utils import timezone

from ..api.serializers import ArticleDetailSerializer
from commons.test import (
    get_profiles,
    get_articles,
)
from django.contrib.auth import get_user_model

User = get_user_model()
FROZEN_TIME_STR = "2022-05-11 12:00:00"
FROZEN_TIME_ARGS = (2022, 5, 11, 12, 0, 0, 0, timezone.utc)


class TestArticleDetailSerializer(TestCase):
    def setUp(self):
        self.profiles = get_profiles(10)
        self.test_profile = self.profiles[0]
        self.articles = get_articles(self.test_profile, 10)
        self.test_article = self.articles[0]

        self.expected_serializer_data = {
            "profile": 1,
            "title": self.test_article.title,
            "slug": self.test_article.slug,
            "content": self.test_article.content.strftime("%Y%m%dT%H:%M:%SZ"),
            "author": self.test_profile.nickname.strftime("%Y%m%dT%H:%M:%SZ"),
            "series": None,
        }

    def test_serializer_잘_생성됨(self):
        serializer = ArticleDetailSerializer(self.articles[0])
        self.assertEqual(serializer.data, self.expected_serializer_data)
