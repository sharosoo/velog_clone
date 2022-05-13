from django.test import TestCase

from commons.test import (
    get_profiles,
    get_articles,
    drf_strftime
)

from ..api.serializers import CommentSerializer


class TestCommentSerializer(TestCase):
    def setUp(self):
        self.profile = get_profiles(1)[0]
        self.article = get_articles(self.profile, 1)[0]
        self.root_comment = self.article.comment
        self.first_comment = self.root_comment.add_child(
            profile=self.profile,
            content='first comment'
        )
        self.expected_first_com_serializer_data = {
            "author": self.profile.nickname,
            "profile": self.profile.pk,
            "content": self.first_comment.content,
            "depth": self.first_comment.depth,
            "created": drf_strftime(self.first_comment.created),
            "modified": drf_strftime(self.first_comment.modified)
        }
        self.second_comment = self.root_comment.add_child(
            profile=self.profile,
            content='second comment'
        )
        self.expected_second_com_serializer_data = {
            "author": self.profile.nickname,
            "profile": self.profile.pk,
            "content": self.second_comment.content,
            "depth": self.second_comment.depth,
            "created": drf_strftime(self.second_comment.created),
            "modified": drf_strftime(self.second_comment.modified)
        }
        self.first_com_comment = self.first_comment.add_child(
            profile=self.profile,
            content='first com comment'
        )
        self.expected_first_com_com_serializer_data = {
            "author": self.profile.nickname,
            "profile": self.profile.pk,
            "content": self.first_com_comment.content,
            "depth": self.first_com_comment.depth,
            "created": drf_strftime(self.first_com_comment.created),
            "modified": drf_strftime(self.first_com_comment.modified)
        }

    def test_first_comment_serializer(self):
        serializer = CommentSerializer(self.first_comment)
        self.assertEqual(serializer.data, self.expected_first_com_serializer_data)

    def test_comments_serializer_in_path_order(self):
        self.expected_comments_serializer_data = [
            self.expected_first_com_serializer_data,
            self.expected_first_com_com_serializer_data,
            self.expected_second_com_serializer_data
        ]

        queryset = self.article.get_related_comments()
        serializer = CommentSerializer(queryset, many=True)

        self.assertEqual(serializer.data, self.expected_comments_serializer_data)


