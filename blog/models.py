from django.contrib.auth.models import AbstractUser
from django.db import models

from blog.utils import DateModelMixin, CounterQuerySetMixin


class User(AbstractUser):
    first_name = models.CharField('Имя', max_length=150, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)

    class Meta(AbstractUser.Meta):
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-id']


class Article(DateModelMixin):
    """
    Модель: Статья
    """
    title = models.CharField('Название', max_length=250)
    author = models.ForeignKey(User, verbose_name='Автор статьи', related_name='articles', on_delete=models.PROTECT)

    objects = CounterQuerySetMixin.as_manager()

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title + ' (' + str(self.pk) + ')'

    def create_comment(self, user, comment=None):
        ArticleComment.objects.create(
            article=self,
            comment=comment,
            user=user,
        )


class ArticleComment(DateModelMixin, models.Model):
    """
    Модель: Комментарий статьи
    """
    comment = models.TextField('Комментарий')
    article = models.ForeignKey(Article, verbose_name='Статья', related_name='comments', on_delete=models.CASCADE)
    parent = models.ForeignKey(
        'self', verbose_name='Родительский комментарий', related_name='comments',
        on_delete=models.CASCADE, blank=True, null=True
    )
    user = models.ForeignKey(User, verbose_name='Пользователь', related_name='article_comments',
                             on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Комментарий статьи'
        verbose_name_plural = 'Комментарии статей'

    def __str__(self):
        return f'Комментарий: {self.comment[:30]}...'


