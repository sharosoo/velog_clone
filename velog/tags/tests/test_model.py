from django.db import IntegrityError
from django.test import TestCase

from ..models import Tag
from django.contrib.auth import get_user_model
from accounts.models import UserProfile
from articles.models import Article

User = get_user_model()


class TagTestCase(TestCase):
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
        self.tag = Tag.objects.create(
            hashtag='test'
        )

    def test_tag(self):
        self.assertTrue(Tag.objects.all().exists())

    def test_article_tagging(self):
        self.article.tags.add(self.tag)
        self.assertEqual(self.tag, self.article.tags.first())

    def test_hashtag_uniqueness(self):
        with self.assertRaises(IntegrityError):
            Tag.objects.create(hashtag='test')

    def test_게시물마다_같은_태그는_한번만(self):
        # with self.assertRaises(IntegrityError): -> IntegrityError
        # db transaction 이전에 validation을 거친다 -> 갯수로 카운트한다.
        self.article.tags.add(self.tag)
        self.assertEqual(1, self.article.tags.count())
