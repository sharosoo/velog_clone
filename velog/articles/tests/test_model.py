import datetime

from django.test import TestCase
from django.utils import timezone

from freezegun import freeze_time

from comments.models import Comment
from series.models import Series
from ..models import Article
from accounts.models import UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()
FROZEN_TIME_STR = "2022-05-11 12:00:00"
FROZEN_TIME_ARGS = (2022, 5, 11, 12, 0, 0, 0, timezone.utc)


class ArticleTestCase(TestCase):

    def setUp(self):
        self.freezer = freeze_time(FROZEN_TIME_STR)
        self.freezer.start()

        self.user = User.objects.create(username='test')
        self.profile = UserProfile.objects.create(
            user=self.user,
            nickname=f'user{self.user.id}',
            desc='test'
        )

        self.article = Article.objects.create(
            profile=self.profile,
            title=f"I'm {self.profile.nickname}",
            slug=f"Im{self.profile.nickname}",
            content="It's test"
        )

        self.article1 = Article.objects.create(
            profile=self.profile,
            title=f"I'm {self.profile.nickname}1",
            slug=f"Im{self.profile.nickname}1",
            content="It's test"
        )

        self.article2 = Article.objects.create(
            profile=self.profile,
            title=f"I'm {self.profile.nickname}2",
            slug=f"Im{self.profile.nickname}2",
            content="It's test"
        )

        self.series = Series.objects.create(
            profile=self.profile,
            title='test'
        )

        self.expected_time = datetime.datetime(*FROZEN_TIME_ARGS)
        self.freezer.stop()

    def test_article이_잘_생성됨(self):
        self.assertEqual(self.article.profile, self.profile)
        self.assertEqual(self.article.title, f"I'm {self.profile.nickname}")
        self.assertEqual(self.article.slug, f"Im{self.profile.nickname}")
        self.assertEqual(self.article.content, "It's test")

        self.assertEqual(self.article.view_cnt, 0)
        self.assertFalse(self.article.series)
        self.assertEqual(self.article.series_order, 0)

        self.assertEqual(self.article.created, self.expected_time)

    def test_article_생성시_root_comment도_생성됨(self):
        self.assertTrue(self.article.comment)
        self.assertEqual(self.article.comment.depth, 1)

        self.assertEqual(self.article.comment.created, self.expected_time)

    def test_article_삭제시_root_comment도_삭제됨(self):
        article_pk = self.article.pk

        comment = self.article.comment
        comment_pk = comment.pk

        self.article.delete()

        self.assertFalse(Article.objects.filter(pk=article_pk).exists())
        self.assertFalse(Comment.objects.filter(pk=comment_pk).exists())

    def test_article_series_생성시_ordering이_잘됨(self):
        self.article.series = self.series
        self.article.save()
        self.assertEqual(self.article.series_order, 1)

        self.article1.series = self.series
        self.article1.save()
        self.assertEqual(self.article1.series_order, 2)

        self.article2.series = self.series
        self.article2.save()
        self.assertEqual(self.article2.series_order, 3)

    def test_article_series_삭제시_article은_삭제되지_않음(self):
        self.series.delete()
        self.assertTrue(Article.objects.all().exists())

    def test_article_series_삭제시_order가_0이됨(self):
        self.assertFalse(Article.objects.filter(series_order__gt=0).exists())
