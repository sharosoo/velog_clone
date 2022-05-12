from django.db import models

from treebeard.mp_tree import MP_Node
from django_extensions.db.models import TimeStampedModel

from accounts.models import UserProfile

# 다른 구현방법 parent, children foreignkey
REMOVED_COMMENT = '삭제된 댓글입니다.'
ROOT_NODE_COMMENT = '루트 노드 댓글입니다.'


class Comment(MP_Node, TimeStampedModel):
    """
    1. 정의
        게시물에 달릴 댓글, 대댓글 model
    2. 구현형태
        tree 구조의 댓글 model

        depth 제한 : 30 ( 31 (255/8) - 1 (root) )
        사이트에서 허용 가능한 총 (root) 댓글 수 (게시물 수와 동일) : 10 ** 12
        게시물당 허용 가능한 댓글 수 : 10 ** 12
    3. 참고사항
        depth=1인 경우 댓글 tree를 관리하기 위한 게시물당 부여되는 가짜 댓글이다.
        active_objects로 쿼리하면 가짜 댓글은 보여주지 않는다.
    """
    # article마다 root 댓글을 하나 생성후 article에서 root 댓글을 foreign key로 가진다.
    # 그 아래에 모든 댓글을 트리 형태로 관리한다.
    # mp_node 적용 이유 ForeignKey -> 'self'로 대댓글 구조를 구현하는 것은 어렵다고 생각했다.
    # 댓글은 article detail view에서 필요한데 comment에서 root node를 제외하고 path를 기준으로 정렬하면 모든 댓글이 순서에 따라 표현된다.
    # 1
    # 1/1, 1/2
    # 2
    # 2/1, 2/2
    # ...
    # root 댓글의 수 (= 게시물의 수) = (허용 가능한 char) ** (steplen)이다.
    steplen = 8

    profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        verbose_name='댓글 작성자 프로필'
    )

    content = models.TextField(
        blank=True,
        default='empty comment',
        verbose_name='댓글 내용'
    )

    active = models.BooleanField(
        blank=True,
        default=True,
        verbose_name='댓글 활성 상태'
    )

    def is_root_comment(self):
        return bool(self.depth == 1)

    def is_root_comment_exists(self):
        return Comment.objects.filter(
            path=self.path[0:self.steplen]
        ).exists()

    def is_leaf_comment(self):
        return self.is_leaf()

    def get_parent_comment(self):
        """
        :returns: the parent node of the current comment object.
            Caches the result in the object itself to help in loops.
        """
        return self.get_parent()

    def get_ancestors_comment(self):
        """
        :returns: A queryset containing the current comment object's ancestors,
            starting by the root node and descending to the parent.
        """
        return self.get_ancestors()

    def get_children_comment(self):
        """:returns: A queryset of all the comment's children comments"""
        return self.get_children()

    def save(self, **kwargs):
        if not self.active:
            self.content = REMOVED_COMMENT if self.depth > 1 else ROOT_NODE_COMMENT

        super(Comment, self).save(**kwargs)

    def delete(self):
        if self.is_root_comment() or self.is_leaf_comment():
            super(Comment, self).delete()

        else:
            self.active = False
            self.save()
