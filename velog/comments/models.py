from django.db import models

from treebeard.mp_tree import MP_Node
from django_extensions.db.models import TimeStampedModel

from accounts.models import UserProfile

# 다른 구현방법 parent, children foreignkey
ROOT_NODE_COMMENT = '루트 노드 댓글입니다.'


class Comment(MP_Node, TimeStampedModel):
    """
    댓글, 대댓글을 관리하기 위한 tree 구조의 댓글 model
    depth 제한 : 30 ( 31 (255/8) - 1 (root) )
    사이트에서 허용 가능한 총 (root) 댓글 수 (게시물 수와 동일) : 10 ** 12
    게시물당 허용 가능한 댓글 수 : 10 ** 12
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

    # profile이 삭제되면 그 profile이 작성한 게시물도 없어져야 한다.
    # Todo: Model Manager로 depth가 2이상인 진짜 comment만 가져오자, field를 추가해서 데이터분석하시는 분들이 읽기 편하게 하자.
    profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
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
