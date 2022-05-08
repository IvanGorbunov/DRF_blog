from rest_framework import status
from rest_framework.response import Response

from blog.filters import ArticleFilter, ArticleDetailFilter
from blog.models import Article, ArticleComment
from blog.serializers import ArticleListSerializer, ArticleDetailSerializer, ArticleCreateEditSerializer, \
    ArticleCommentSerializer, ArticleCommentCreateSerializer, ArticleCommentUpdateSerializer
from blog.utils import MultiSerializerViewSet, find_child


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
    serializers = {
        'list': ArticleCommentSerializer,
        'create': ArticleCommentCreateSerializer,
        'update': ArticleCommentUpdateSerializer,
    }

    def list(self, request, *args, **kwargs):
        """
        Список комментариев к статье
        """
        # return super().list(request, *args, **kwargs)
        comments = ArticleComment.objects.raw('''
            WITH RECURSIVE down_search(id, article_id, comment, parent_id, level) AS (
                SELECT 
                    id
                    ,article_id
                    ,comment
                    ,parent_id
                    ,level
                    ,TRUE as is_root
                    ,user_id
                    ,create_dt
                FROM blog_articlecomment
                WHERE article_id = ''' + str(kwargs['pk']) + '''
                    AND level = 0
                UNION ALL
                SELECT
                    child.id
                    ,child.article_id
                    ,child.comment
                    ,child.parent_id
                    ,child.level
                    ,FALSE as is_root
                    ,child.user_id
                    ,child.create_dt
                FROM blog_articlecomment AS child, down_search AS parent
                WHERE child.parent_id = parent.id
                )
            SELECT * FROM down_search
            WHERE level < 3   
        ''')

        context = {}
        for item in comments:  # type ArticleComment
            if item.is_root:
                context = {
                    'id': item.id,
                    'article_id': item.article_id,
                    'comment': item.comment,
                    'parent_id': item.parent_id,
                    'level': item.level,
                    'is_root': item.is_root,
                    'user_id': item.user_id,
                    'create_dt': item.create_dt,
                    'children': [],
                }
        if not context:
            return Response(status=status.HTTP_404_NOT_FOUND)

        find_child(context, comments)

        return Response(context, status=status.HTTP_200_OK)

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

    def retrieve(self, request, *args, **kwargs):
        """
        Просмотр комментария
        """

        comments = ArticleComment.objects.raw('''
            WITH RECURSIVE down_search(id, article_id, comment, parent_id, level) AS (
                SELECT 
                    id
                    ,article_id
                    ,comment
                    ,parent_id
                    ,level
                    ,TRUE as is_root
                    ,user_id
                    ,create_dt
                FROM blog_articlecomment
                WHERE id = ''' + str(kwargs['pk']) + '''
                UNION ALL
                SELECT
                    child.id
                    ,child.article_id
                    ,child.comment
                    ,child.parent_id
                    ,child.level
                    ,FALSE as is_root
                    ,child.user_id
                    ,child.create_dt
                FROM blog_articlecomment AS child, down_search AS parent
                WHERE child.parent_id = parent.id
                )
            SELECT * FROM down_search   
        ''')

        context = {}
        for item in comments:  # type ArticleComment
            if item.is_root:
                context = {
                    'id': item.id,
                    'article_id': item.article_id,
                    'comment': item.comment,
                    'parent_id': item.parent_id,
                    'level': item.level,
                    'is_root': item.is_root,
                    'user_id': item.user_id,
                    'create_dt': item.create_dt,
                    'children': [],
                }
        if not context:
            return Response(status=status.HTTP_404_NOT_FOUND)

        find_child(context, comments)

        return Response(context, status=status.HTTP_200_OK)

