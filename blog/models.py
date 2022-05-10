from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import OuterRef, Subquery, Count, Q
from mptt.models import MPTTModel, TreeForeignKey


class User(AbstractUser):
    first_name = models.CharField('Имя', max_length=150, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)

    class Meta(AbstractUser.Meta):
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-id']


class CreateModelMixin(models.Model):
    create_dt = models.DateTimeField('Создание записи', auto_now_add=True)

    class Meta:
        abstract = True


class DateModelMixin(CreateModelMixin, models.Model):

    change_dt = models.DateTimeField('Изменение записи', auto_now=True)

    class Meta:
        abstract = True


class SubqueryAggregate:
    """
    Класс для агрегаций в подзапросах
    """
    def __init__(self, sub_model, aggregate, name, filters=None) -> None:
        self.sub_model = sub_model
        self.aggregate = aggregate
        self.name = name
        self.filters = filters or Q()
        super().__init__()

    def subquery(self):
        query = self.sub_model.objects.filter(
            self.filters,
            **{self.name: OuterRef('pk')},
        ).values(self.name).annotate(annotate_value=self.aggregate('pk')).values('annotate_value')
        return Subquery(query)


class CounterQuerySetMixin(models.QuerySet):
    def annotate_comments_count(self):
        """
        Анотация количества комментариев
        """
        field = self.model.comments.field
        sub_class = SubqueryAggregate(field.model, Count, field.name)
        return self.annotate(comments_count=sub_class.subquery())


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

    def get_count_comments(self):
        return f'{self.comments.all().count()}'

    def create_comment(self, user, comment=None):
        ArticleComment.objects.create(
            article=self,
            comment=comment,
            user=user,
        )


class ArticleComment(DateModelMixin, MPTTModel):
    """
    Модель: Комментарий статьи
    """
    comment = models.TextField('Комментарий')
    article = models.ForeignKey(Article, verbose_name='Статья', related_name='comments', on_delete=models.CASCADE)

    parent = TreeForeignKey(
        'self',
        verbose_name='Родительский комментарий',
        related_name='children',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    user = models.ForeignKey(User, verbose_name='Пользователь', related_name='article_comments',
                             on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Комментарий статьи'
        verbose_name_plural = 'Комментарии статей'

    def __str__(self):
        return f'Комментарий: {self.comment[:30]}...'





