from rest_framework import serializers

from comments.api.serializers import CommentSerializer
from tags.models import Tag
from ..models import Article


class ArticleDetailSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField()
    comments = serializers.JSONField(source='get_related_comments_dict', read_only=True)

    class Meta:
        model = Article

        fields = [
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
            'tags'
        ]
