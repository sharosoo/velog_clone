from django.db import models
from django.conf import settings
from django_extensions.db.models import TimeStampedModel


class UserProfile(TimeStampedModel):
    """
    django 기본 인증 user model은 건드리지 않고 one-to-one으로 확장해서 필요한 필드들을 관리하기 위한 Profile Model
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        # 계정 삭제시 user를 delete하면 profile도 따라서 없어져야함.
        on_delete=models.CASCADE,
    )

    nickname = models.CharField(
        max_length=16,
        unique=True,
        verbose_name='닉네임'
    )

    desc = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='자기소개'
    )
