from rest_framework import serializers

from tags.models import Tag
from ..models import Article


class ArticleDetailSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField()
    comments = serializers.ReadOnlyField(source='get_related_comments_dict')
    # implement TagSerializer
    # append series

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
            'comment',
            'comments',
        ]
