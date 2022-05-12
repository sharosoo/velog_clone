from django.db import models
from django.db.models import Max
from django.utils.functional import cached_property

from django_extensions.db.models import TimeStampedModel

from series.models import Series
from comments.models import Comment


class Article(TimeStampedModel):
    """
    게시물을 표현하기 위한 모델
    """

    profile = models.ForeignKey(
        'accounts.UserProfile',
        on_delete=models.CASCADE,
        related_name='article',
        verbose_name='프로필'
    )

    title = models.CharField(
        max_length=60,
        verbose_name='제목'
    )

    # URL source에서 article의 주소를 사람이 읽을 수 있는 형태로 고치기 위해 slugify를 이용한다.
    # frontend 에서 form에 입력된 title을 자동 변환(영어,숫자,-로 구성, 공백 없음)하여 slug도 함께 제출하는 것을 가정했다.
    # Todo: slug field를 blank=True로 고치고 backend에서 slug가 blank인 경우 slug를 자동 변환해주는 로직을 추가하자.
    # Todo: Title이 영어나 숫자로 구성되지 않은 경우 번역하여 slug를 저장하자.(URL은 ASCII 코드로 전송이 가능하다)
    # Todo: title이 겹치는 경우도 slug를 구별되도록 설정하는 것이 좋다.
    slug = models.SlugField(
        max_length=60,
        # blank=True,
        # default = slugify function()
        verbose_name='슬러그'
    )

    # Todo: editor 구현을 위해 markdownx 필드로 변경 필요
    # 구현을 쉽게 하기 위해 우선은 TextField로 두자. markdownx필드는 TextField기반이므로 변경이 쉬울 것으로 예상된다.
    content = models.TextField(
        verbose_name='내용'
    )

    # view_cnt는 항상 0이상
    # 사용자가 입력하면 안됨 readonly
    # ArticleViewCnt 모델에서 조회가 될때마다 1씩 추가해준다.
    # 꼭 필요한 필드는 아니지만 page마다 빈번하게 조회되는 쿼리이므로 반정규화했다.
    view_cnt = models.PositiveIntegerField(
        blank=True,
        default=0,
        verbose_name='조회수'
    )

    # like_cnt는 항상 0이상
    # Like 모델에서 생성 될때마다 1씩 추가해준다.
    # 꼭 필요한 필드 아니지만 page마다 빈번하게 조회되는 쿼리이므로 반정규화했다.
    like_cnt = models.PositiveIntegerField(
        blank=True,
        default=0,
        verbose_name='좋아요수'
    )

    # series_order를 통해 series내의 게시물 순서를 결정한다. (0: series 아님, 1~ : 각자의 series에서 series order)
    # Todo: 노출순서 설정 더 고민해보기, Manager로 잘 감싸자
    series_order = models.PositiveIntegerField(
        blank=True,
        default=0,
        verbose_name='시리즈 순서'
    )

    # series가 삭제된다 하더라도 그 하위에 있던 게시물은 삭제가 되면 안된다.
    series = models.ForeignKey(
        Series,
        on_delete=models.SET_NULL,
        related_name='article',
        blank=True,
        null=True,
        verbose_name='시리즈'
    )

    # article에 달린 comment(트리구조)의 root를 가리킨다.
    comment = models.ForeignKey(
        Comment,
        # 게시물이 삭제되기 전에 root 댓글(가짜 댓글)이 삭제될 일은 없다.
        # 그래도 article이 삭제 되면 위험하니 SET_NULL로 하자.
        on_delete=models.SET_NULL,
        related_name='article',
        editable=False,
        blank=True,
        null=True,
        verbose_name='댓글'
    )

    class Meta:
        # 원하는 article detail url은 /profile_nickname/slug이므로 미리 추가해놓은 제한사항
        constraints = [
            models.UniqueConstraint(
                fields=['profile', 'slug'],
                name='unique slug for profile'
            ),
        ]

    @cached_property
    def author(self):
        return self.get_author()

    def get_author(self):
        return f'{self.profile.nickname}'

    def get_max_series_order(self):
        queryset = Article.objects.filter(
            series=self.series
        )

        if not queryset.exists():
            return 0

        ret = queryset.aggregate(
            Max('series_order')
        )['series_order__max']

        return ret

    def save(self, **kwargs):
        if not self.comment:
            self.comment = Comment.add_root(profile=self.profile, active=False)

        if self.series:
            if not self.series_order:
                max_order = self.get_max_series_order()
                self.series_order = max_order + 1

        elif self.series_order:
            self.series_order = 0

        super(Article, self).save(**kwargs)

    def delete(self, using=None, keep_parents=False):
        if self.comment:
            self.comment.delete()
        super(Article, self).delete()
