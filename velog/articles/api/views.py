from django.shortcuts import get_object_or_404
from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView

from articles.api.serializers import ArticleDetailSerializer
from articles.models import Article
from articleviews.models import ArticleViewCount


class ArticleDetailView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = ArticleDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        article_id = kwargs.get('article_id', 0)
        instance = get_object_or_404(
            Article,
            id=article_id
        )
        ArticleViewCount.objects.create(
            article=instance
        )
        ret = ArticleDetailSerializer(instance)
        return Response(data=ret.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        article_id = kwargs.get('article_id', 0)
        instance = get_object_or_404(
            Article,
            id=article_id
        )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, *args, **kwargs):
        article_id = kwargs.get('article_id', 0)
        instance = get_object_or_404(
            Article,
            id=article_id
        )
        serializer = ArticleDetailSerializer(data=request.data)
        if serializer.is_valid():
            instance.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
