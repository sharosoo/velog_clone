from django.db import models

from django_extensions.db.models import TimeStampedModel

from accounts.models import UserProfile


class Series(TimeStampedModel):
    """
    Series: 여러 article들의 공통 주제
    UserProfile에 귀속됨
    """
    title = models.CharField(
        max_length=60
    )

    profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='series'
    )
