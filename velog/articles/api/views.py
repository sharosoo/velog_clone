from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView

from rest_framework.response import Response
from rest_framework.views import APIView

from articles.api.serializers import ArticleDetailSerializer, ArticleListSerializer
from articles.models import Article
from articleviews.models import ArticleViewCount
from recommends.models import RecommendMonthly, RecommendWeekly, RecommendToday


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


# Todo: Default_pagination_class를 cursor pagination으로 설정 후 각각 cursor pagination class를 오버라이드해서 명시해놓기
# Todo: ListView들 테스트해보기
class ArticleRecentListView(ListAPIView):
    serializer_class = ArticleListSerializer

    def get_queryset(self):
        # order by pagination에서 구현하고 빼야됨.
        return Article.objects.all().order_by('-created')


class ArticleRecommendListView(ListAPIView):
    # Todo: 각각의 Recommend model에 대한 serializer를 만들어야 하는데
    #   하나의 base serializer를 상속하는 방법이 적합해보인다.
    serializer_class = ArticleListSerializer

    def get_queryset(self):
        # monthly, weekly, today
        recommend_type = self.kwargs.get('recommend_type', default='weekly')

        if recommend_type not in ('monthly', 'weekly', 'today'):
            return Article.objects.all().order_by('-created')

        elif recommend_type == 'monthly':
            return RecommendMonthly.objects.all().order_by('-recommendation')

        elif recommend_type == 'weekly':
            return RecommendWeekly.objects.all().order_by('-recommendation')

        else:
            return RecommendToday.objects.all().order_by('-recommendation')

class ArticleSearchListView(ListAPIView):
    serializer_class = ArticleListSerializer

    def get_queryset(self):
        # Todo: request.queryparam에서 쿼리스트링으로 search하려고 했던 dict 변수들을 iterate한다.
        #   raw SQL을 이용해 변수들을 한번에 filter하고 raw queryset으로 돌려주는 것이 최선인 것 같다.
        return Article.objects.all()




