from django.db import models

from django_extensions.db.models import TimeStampedModel

from accounts.models import UserProfile
from articles.models import Article


class Like(TimeStampedModel):
    """
    user마다 각 article에 좋아요를 누를 수 있는 기능을 구현한 모델
    """
    # unlike하면 어차피 DB에서 삭제할거라서 굳이 modified 필드가 필요 없기는 하다.

    profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='like'
    )

    class Meta:
        # 좋아요는 각 article에 대해 user마다 한번씩만 누를 수 있다.
        constraints = [
            models.UniqueConstraint(
                fields=['profile', 'article'],
                name='unique like'
            ),
        ]
        # like 모델을 검색할때 기간에 따른 article의 좋아요 수를 자주 검색하게 된다.
        # 따라서 multi column에 대해 bool형태의 비트맵으로 쿼리하도록 multi column index를 적용하자
        # Todo: multi column index 순서에 맞게 쿼리해야 하므로 따로 manager와 메소드를 만들어두자.
        indexes = [
            models.Index(
                fields=['article'], name='article_idx'
            ),
            models.Index(
                fields=['article', 'created'], name='article_period_like_idx'
            ),
        ]
