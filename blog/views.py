from rest_framework import status
from rest_framework.response import Response

from blog.filters import ArticleFilter, ArticleDetailFilter, ArticleCommentFilter
from blog.models import Article, ArticleComment
from blog.serializers import ArticleListSerializer, ArticleDetailSerializer, ArticleCreateEditSerializer, \
    ArticleCommentSerializer, ArticleCommentCreateSerializer, ArticleCommentUpdateSerializer
from blog.utils import MultiSerializerViewSet


class ArticleViewSet(MultiSerializerViewSet):
    queryset = Article.objects.all()
    filtersets = {
        'list': ArticleFilter,
        'retrieve': ArticleDetailFilter,
    }
    serializers = {
        'list': ArticleListSerializer,
        'retrieve': ArticleDetailSerializer,
        'create': ArticleCreateEditSerializer,
        'update': ArticleCreateEditSerializer,
        'partial_update': ArticleCreateEditSerializer,
    }

    def list(self, request, *args, **kwargs):
        """
        Список статей
        """
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Создание статьи
        """
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Просмотр статьи
        """
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Полное редактирование статьи
        """
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Частичное редактироание статьи
        """
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Удаление статьи
        """
        article = self.get_object()
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ArticleCommentViewSet(MultiSerializerViewSet):
    queryset = ArticleComment.objects.all()
    filtersets = {
        'list': ArticleCommentFilter,
    }
    serializers = {
        'list': ArticleCommentSerializer,
        'create': ArticleCommentCreateSerializer,
        'update': ArticleCommentUpdateSerializer,
    }

    def list(self, request, *args, **kwargs):
        """
        Список комментариев к статье
        """
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Создание комментария к статье
        """
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Редактирование комментария
        """
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Удаление комментария
        """
        return super().destroy(request, *args, **kwargs)


class CommentViewSet(MultiSerializerViewSet):
    queryset = ArticleComment.objects.all()
    filtersets = {
        'list': ArticleCommentFilter,
    }
    serializers = {
        'retrieve': ArticleCommentSerializer,
    }

    def retrieve(self, request, *args, **kwargs):
        """
        Просмотр статьи
        """
        return super().retrieve(request, *args, **kwargs)
