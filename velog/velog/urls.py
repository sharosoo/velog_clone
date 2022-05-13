from django.contrib import admin
from django.urls import path, include

from articles.api.views import ArticleDetailView
from likes.views import LikeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/article/', ArticleDetailView.as_view()),
    path('api/article/like/', LikeView.as_view()),
    path('api/article/<int:article_id>/', ArticleDetailView.as_view()),
]
