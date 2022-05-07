from django_filters.rest_framework import FilterSet

from blog.models import Article, ArticleComment
from blog.utils import SearchFilterSet


class ArticleFilter(SearchFilterSet):
    """
    Фильтр статей
    """
    search_fields = ('title',)

    class Meta:
        model = Article
        fields = (
        )


class ArticleDetailFilter(FilterSet):
    """
    Фильтр просмотра
    """
    class Meta:
        model = Article
        fields = (
        )

    def filter_queryset(self, queryset):
        qs = super().filter_queryset(queryset)
        qs = qs.annotate_comments_count()
        qs = qs.select_related(
            'author',
        )
        return qs
