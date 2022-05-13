from rest_framework import serializers

from ..models import Comment


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField()

    class Meta:
        model = Comment

        fields = [
            'author',
            'profile',
            'content',
            'depth',
            'created',
            'modified'
        ]
