from rest_framework import serializers

from comments.api.serializers import CommentSerializer
from tags.models import Tag
from ..models import Article


class ArticleDetailSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField()
    # queryset을 이용해 JSON안에 JSON 형태로 만들고 싶었으나 이렇게 설정하는 경우 출력이 dict 형태로 나옴.
    comments = serializers.JSONField(source='get_related_comments_dict', read_only=True)
    # Todo: tags도 같이 보내기
    #  many to many field를 직접 serialize하는 것은 pk관련 오류가 발생하여 이후 수정 필요

    class Meta:
        model = Article

        fields = [
            'pk',
            'slug',
            'title',
            'author',
            'profile',
            'created',
            'view_cnt',
            'like_cnt',
            'content',
            'series',
            'series_order',
            'root_comment',
            'comments',
        ]
