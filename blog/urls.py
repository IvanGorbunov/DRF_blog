from django.urls import path

from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.ArticleViewSet.as_view({'get': 'list', 'post': 'create'}), name='crticle_list'),
    path('<int:pk>/', views.ArticleViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='manage'),

    path('<int:pk>/comments/', views.ArticleCommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='comments'),
    # path('comments/<int:pk>/', views.CommentViewSet.as_view({'get': 'retrieve', }), name='comments'),
]
