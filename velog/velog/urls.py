from django.contrib import admin
from django.urls import path, include

import articles.api.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/article/', articles.api.views.ArticleCreateView.as_view())
]
