from django.test import TestCase

from comments.models import Comment
from ..models import Article
from accounts.models import UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()


class ArticleTestCase(TestCase):
    def setUp(self):

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

    def test_article이_잘_생성됨(self):
        self.assertEqual(self.article.profile, self.profile)
        self.assertEqual(self.article.title, f"I'm {self.profile.nickname}")
        self.assertEqual(self.article.slug, f"Im{self.profile.nickname}")
        self.assertEqual(self.article.content, "It's test")
        self.assertEqual(self.article.view_cnt, 0)
        self.assertFalse(self.article.series)
        self.assertEqual(self.article.series_order, 0)

    def test_article_생성시_root_comment도_생성됨(self):
        self.assertTrue(self.article.comment)
        self.assertEqual(self.article.comment.depth, 1)

    def test_article_삭제시_root_comment도_삭제됨(self):
        article_pk = self.article.pk
        comment = self.article.comment
        comment_pk = comment.pk
        self.article.delete()
        self.assertFalse(Article.objects.filter(pk=article_pk).exists())
        self.assertFalse(Comment.objects.filter(pk=comment_pk).exists())
