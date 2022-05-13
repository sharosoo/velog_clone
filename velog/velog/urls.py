from django.contrib import admin
from django.urls import path, include

from articles.api.views import ArticleDetailView
from likes.views import LikeView, UnlikeView

urlpatterns = [
    path(route='admin/', view=admin.site.urls),
    path(route='api/article/', view=ArticleDetailView.as_view()),
    path(route='api/article/<int:article_id>/', view=ArticleDetailView.as_view()),
    path(route='api/like/', view=LikeView.as_view()),
    path(route='api/unlike/', view=UnlikeView.as_view()),
]
