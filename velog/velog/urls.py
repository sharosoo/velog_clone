from django.contrib import admin
from django.urls import path, include

from articles.api.views import ArticleDetailView
from likes.views import LikeView, UnlikeView
from series.views import SeriesDetailView, SeriesAddView

urlpatterns = [
    path(route='admin/', view=admin.site.urls),
    path(route='api/article/', view=ArticleDetailView.as_view()),
    path(route='api/article/<int:article_id>/', view=ArticleDetailView.as_view()),
    path(route='api/like/', view=LikeView.as_view()),
    path(route='api/unlike/', view=UnlikeView.as_view()),
    path(route='api/series/', view=SeriesDetailView.as_view()),
    path(route='api/series/<int:series_id>/', view=SeriesDetailView.as_view()),
    path(route='api/series/add/', view=SeriesAddView.as_view())
]
