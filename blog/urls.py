from django.urls import path

from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.ArticleViewSet.as_view({'get': 'list', 'post': 'create'}), name='crticle_list'),
]
