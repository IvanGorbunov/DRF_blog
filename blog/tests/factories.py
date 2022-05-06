from string import ascii_lowercase

from factory import SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText

from blog.models import User, Article, ArticleComment


class UserFactory(DjangoModelFactory):
    """
    Фабрика Пользователя
    """
    class Meta:
        model = User

    username = FuzzyText(length=12, chars=ascii_lowercase)
    first_name = FuzzyText(length=12, chars=ascii_lowercase)
    last_name = FuzzyText(length=12, chars=ascii_lowercase)


class ArticleFactory(DjangoModelFactory):
    """
    Фабрика статьи
    """
    class Meta:
        model = Article

    title = FuzzyText(length=50)
    author = SubFactory(UserFactory)


class ArticleCommentFactory(DjangoModelFactory):
    """
    Фабрика коментария к статье
    """
    class Meta:
        model = ArticleComment

    comment = FuzzyText(length=50)
    article = SubFactory(ArticleFactory)
    user = SubFactory(UserFactory)
