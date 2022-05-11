from django.db import models

from treebeard.mp_tree import MP_Node
from django_extensions.db.models import TimeStampedModel

from accounts.models import UserProfile


class Comment(MP_Node, TimeStampedModel):
    """
    댓글, 대댓글을 관리하기 위한 tree 구조의 댓글 model
    depth 제한 : 30 ( 31 (255/8) - 1 (root) )
    사이트에서 허용 가능한 총 (root) 댓글 수 (게시물 수와 동일) : 10 ** 12
    게시물당 허용 가능한 댓글 수 : 10 ** 12
    """
    # mp_node 적용 이유 ForeignKey -> 'self'로 하는 경우 대댓글 구조를 다시
    node_order_by = ['created']
    steplen = 8
    # article마다 root 댓글을 하나 생성후 article에서 root 댓글을 foreign key로 가진다.
    # comment는 그 자체를 쿼리하는 경우는 없고 article에 종속적인 개념이다.
    # 그 아래에 모든 댓글을 트리 형태로 관리한다.

    profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )

    content = models.TextField(
        blank=True,
        default='empty comment'
    )
