from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView

from articles.models import Article
from likes.models import Like


class LikeView(APIView):

    def post(self, request, *args, **kwargs):

        article_id = request.data.get('article_id', 0)

        if (profile_id := request.data.get('profile_id', 0)) is False:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        try:
            Like.objects.create(
                profile_id=profile_id,
                article_id=article_id
            )
            return Response(status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UnlikeView(APIView):

    def post(self, request, *args, **kwargs):

        article_id = request.data.get('article_id', 0)

        if (profile_id := request.data.get('profile_id', 0)) is False:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        like_instance = get_object_or_404(
            Like,
            profile_id=profile_id,
            article_id=article_id
        )

        try:
            like_instance.delete()
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)
