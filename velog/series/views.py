from django.shortcuts import get_object_or_404
from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView

from articles.api.serializers import ArticleDetailSerializer
from articles.models import Article
from series.api.serializers import SeriesSerializer
from series.models import Series


class SeriesDetailView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = SeriesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        series_id = kwargs.get('series_id', 0)
        instance = get_object_or_404(
            Series,
            id=series_id
        )
        ret = SeriesSerializer(instance)
        return Response(data=ret.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        series_id = kwargs.get('series_id', 0)
        profile_id = request.data.get('profile_id', 0)
        instance = get_object_or_404(
            Series,
            id=series_id
        )
        if instance.profile_id != profile_id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        try:
            instance.delete()
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, *args, **kwargs):
        series_id = kwargs.get('series_id', 0)
        instance = get_object_or_404(
            Series,
            id=series_id
        )
        profile_id = request.data.get("profile", 0)
        if profile_id != instance.profile_id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = SeriesSerializer(data=request.data)
        if serializer.is_valid():
            instance.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SeriesAddView(APIView):

    def post(self, request, *args, **kwargs):
        series_id = request.data.get('series_id', 0)
        profile_id = request.data.get('profile', 0)
        article_id = request.data.get('article', 0)

        series_instance = get_object_or_404(
            Series,
            id=series_id
        )

        article_instance = get_object_or_404(
            Article,
            id=article_id
        )

        if series_instance.profile_id != profile_id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if article_instance.profile_id != profile_id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        try:
            article_instance.series = series_instance
            article_instance.save()
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = ArticleDetailSerializer(article_instance)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        profile_id = request.data.get('series_id', 0)
        article_id = request.data.get('series_id', 0)

        article_instance = get_object_or_404(
            Article,
            id=article_id
        )
        if article_instance.profile_id != profile_id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        try:
            article_instance.series = None
            article_instance.save()
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = ArticleDetailSerializer(article_instance)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
