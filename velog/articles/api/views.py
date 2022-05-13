from django.shortcuts import get_object_or_404
from rest_framework import generics

from rest_framework.response import Response
from rest_framework.views import APIView

from articles.api.serializers import ArticleDetailSerializer


class ArticleCreateView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = ArticleDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class GenericArticleCreateView(generics.CreateAPIView):
    serializer_class = ArticleDetailSerializer
