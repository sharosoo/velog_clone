from django.test import TestCase
from django.utils import timezone

from tags.models import Tag
from ..api.serializers import ArticleDetailSerializer
from commons.test import (
    get_profiles, drf_strftime,
    get_articles, nested_drf_strftime,
)
from django.contrib.auth import get_user_model

User = get_user_model()
FROZEN_TIME_STR = "2022-05-11 12:00:00"
FROZEN_TIME_ARGS = (2022, 5, 11, 12, 0, 0, 0, timezone.utc)


def get_comments_dict(obj):
    return f'["{obj.profile.nickname}", {obj.profile.pk}, "{obj.content}", {obj.depth}, "{nested_drf_strftime(obj.created)}", "{nested_drf_strftime(obj.modified)}"]'


class TestArticleDetailSerializer(TestCase):
    def setUp(self):
        self.profiles = get_profiles(10)
        self.test_profile = self.profiles[0]
        self.articles = get_articles(self.test_profile, 10)
        self.test_article = self.articles[0]
        self.root_comment = self.test_article.root_comment
        self.first_comment = self.root_comment.add_child(
            profile=self.test_profile,
            content='first comment'
        )
        self.second_comment = self.root_comment.add_child(
            profile=self.test_profile,
            content='second comment'
        )
        self.first_com_comment = self.first_comment.add_child(
            profile=self.test_profile,
            content='first com comment'
        )

        self.first_tag = Tag.objects.create(
            hashtag='test1'
        )
        self.second_tag = Tag.objects.create(
            hashtag='test2'
        )

        self.test_article.tags.add(self.first_tag, self.second_tag)

        self.expected_serializer_data = {
            "profile": 1,
            "title": self.test_article.title,
            "slug": self.test_article.slug,
            "content": self.test_article.content,
            "author": self.test_profile.nickname,
            "series": None,
            "created": drf_strftime(self.test_article.created),
        }

    def test_serializer_잘_생성됨(self):
        serializer = ArticleDetailSerializer(self.articles[0])
        self.comments_dict = '['
        self.comments_dict += get_comments_dict(self.first_comment)
        self.comments_dict += ', '
        self.comments_dict += get_comments_dict(self.first_com_comment)
        self.comments_dict += ', '
        self.comments_dict += get_comments_dict(self.second_comment)
        self.comments_dict += ']'

        self.assertEqual(serializer.data["profile"], self.expected_serializer_data["profile"])
        self.assertEqual(serializer.data["title"], self.expected_serializer_data["title"])
        self.assertEqual(serializer.data["slug"], self.expected_serializer_data["slug"])
        self.assertEqual(serializer.data["content"], self.expected_serializer_data["content"])
        self.assertEqual(serializer.data["author"], self.expected_serializer_data["author"])
        self.assertEqual(serializer.data["author"], self.expected_serializer_data["author"])
        self.assertEqual(serializer.data["series"], self.expected_serializer_data["series"])
        self.assertEqual(serializer.data["created"], self.expected_serializer_data["created"])
        self.assertEqual(serializer.data["view_cnt"], 0)
        self.assertEqual(serializer.data["like_cnt"], 0)
        self.assertEqual(serializer.data["root_comment"], self.root_comment.pk)
        self.assertEqual(serializer.data["comments"], self.comments_dict)
        self.assertEqual(serializer.data["tags"], [1, 2])






