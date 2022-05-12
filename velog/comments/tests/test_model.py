from django.test import TestCase

from ..models import Comment, REMOVED_COMMENT
from articles.models import Article
from accounts.models import UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()


class CommentTestCase(TestCase):
    def setUp(self):

        self.user = User.objects.create(
            username='test'
        )

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

        self.first_comment = self.article.comment.add_child(
            profile=self.profile,
            content='첫번째 댓글입니다.'
        )

        self.first_com_comment = self.first_comment.add_child(
            profile=self.profile,
            content='첫번째 대댓글입니다.'
        )

        self.first_com_com_comment = self.first_com_comment.add_child(
            profile=self.profile,
            content='첫번째 대대댓글입니다.'
        )

        self.second_com_comment = self.first_comment.add_child(
            profile=self.profile,
            content='두번째 대댓글입니다.'
        )

    def test_comment의_depth가_잘_저장됨(self):
        self.assertEqual(self.first_comment.depth, 2)
        self.assertEqual(self.first_com_comment.depth, 3)
        self.assertEqual(self.first_com_com_comment.depth, 4)
        self.assertEqual(self.second_com_comment.depth, 3)

    def test_inner_node인_commnet가_삭제되면_안됨(self):
        inner_node_pk = self.first_com_comment.pk
        self.first_com_comment.delete()
        inner_node_comment_queryset = Comment.objects.filter(
            pk=inner_node_pk
        )
        self.assertTrue(inner_node_comment_queryset.exists())
        inner_node_comment = inner_node_comment_queryset[0]
        self.assertFalse(inner_node_comment.active)
        self.assertEqual(inner_node_comment.content, REMOVED_COMMENT)

    def test_inner_node삭제시_child_node가_삭제되면_안됨(self):
        child_node_pk = self.first_com_com_comment.pk
        self.first_com_comment.delete()

        child_node_queryset = Comment.objects.filter(pk=child_node_pk)
        self.assertTrue(child_node_queryset.exists())

        child_node = child_node_queryset[0]
        self.assertTrue(child_node.active)
        self.assertNotEqual(child_node.content, REMOVED_COMMENT)

    def test_root_node삭제시_모든_comment가_삭제됨(self):
        self.article.comment.delete()
        self.assertFalse(Comment.objects.all().exists())

    def test_leaf_node삭제시_삭제되어야함(self):
        leaf_node_pk = self.first_com_com_comment.pk
        self.first_com_com_comment.delete()

        leaf_node_queryset = Comment.objects.filter(pk=leaf_node_pk)
        self.assertFalse(leaf_node_queryset.exists())
