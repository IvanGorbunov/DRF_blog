from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from blog.models import User, Article, ArticleComment


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    verbose_name_plural = 'Пользователи'
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
    )
    list_per_page = 25
    fieldsets = (
        (
            None, {
                'fields': ('username', 'password')
            }
        ),
        (
            _('User data'), {
                'fields': ('first_name', 'last_name',)
            }
        ),
        (
            _('Important dates'), {
                'fields': ('last_login', 'date_joined')
            }
        ),
    )
    list_display_links = (
        'username',
        'first_name',
        'last_name',
    )


class ArticleCommentInline(TabularInline):
    raw_id_fields = ('parent', 'user', 'article',)
    model = ArticleComment
    extra = 0
    verbose_name_plural = 'Коментарии'
    fieldsets = (
        (
            None, {
                'fields': (
                    'article',
                    'user',
                    'parent',
                    'level',
                    'comment',
                )
            }
        ),
    )


@admin.register(Article)
class ArticleAdmin(ModelAdmin):
    verbose_name_plural = 'Статьи'
    inlines = (
        ArticleCommentInline,
    )
    list_display = (
        'id',
        'title',
        'create_dt',
        'change_dt',
    )
    list_per_page = 25
    fieldsets = (
        (
            None, {
                'fields': (
                    'title',
                )
            }
        ),
    )
    list_display_links = (
        'id',
        'title',
    )


@admin.register(ArticleComment)
class ArticleCommentAdmin(ModelAdmin):
    verbose_name_plural = 'Комментарии статей'
    raw_id_fields = ('parent', 'user', 'article')
    list_display = ('id', 'comment', 'parent', 'level', 'user', 'article', )
    search_fields = ('id', 'comment', )
    fieldsets = (
        (
            None, {
                'fields': (
                    'article',
                    'user',
                    'parent',
                    'level',
                    'comment',
                )
            }
        ),
    )
