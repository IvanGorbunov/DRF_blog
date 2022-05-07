from rest_framework.reverse import reverse_lazy
from rest_framework.utils import json

from blog.models import Article, ArticleComment
from blog.tests.factories import UserFactory, ArticleFactory, ArticleCommentFactory
from blog.utils import WithLoginTestCase


class ArticleViewTest(WithLoginTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self) -> None:
        super().setUp()
        self.user_1 = UserFactory()
        self.user_2 = UserFactory()
        self.article = ArticleFactory(author=self.user_1)

    def test_list(self):
        url = reverse_lazy('blog:article_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), Article.objects.all().count(), response.data)

    def test_create(self):
        url = reverse_lazy('blog:article_list')
        data = {
            'title': 'Название',
        }
        response = self.client.post(url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.data), Article.objects.all().count(), response.data)

    def test_retrieve(self):
        url = reverse_lazy('blog:manage', kwargs=dict(pk=self.article.pk))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data['id'], self.article.pk, response.data)

    def test_edit(self):
        self.auth_user(self.user_2)
        url = reverse_lazy('blog:manage', kwargs=dict(pk=self.article.pk))
        data = {
            'title': 'Название',
            'author': self.user_2.pk,
        }
        response = self.client.put(url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200, response.data)
        article = Article.objects.filter(pk=response.data['id']).values('title', 'author')[0]
        for check_field in data.keys():
            self.assertEqual(article[check_field], data[check_field])

    def test_delete(self):
        url = reverse_lazy('blog:manage', kwargs=dict(pk=self.article.pk))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204, response.data)
        article = Article.objects.filter(pk=self.article.pk)  # type: Article
        self.assertIsNone(article.first())


class ArticleCommentViewTest(WithLoginTestCase):

    def test_list(self):
        comment = ArticleCommentFactory()
        child_comment = ArticleCommentFactory(parent=comment)
        child_child_comment = ArticleCommentFactory(parent=child_comment)

        url = reverse_lazy('blog:comments_list', kwargs=dict(pk=comment.article_id))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        result_comment = response.data
        result_child_comment = result_comment['children'][0]
        result_child_child_comment = result_child_comment['children'][0]
        self.assertEqual(result_comment['comment'], comment.comment, response.data)
        self.assertEqual(result_child_comment['comment'], child_comment.comment, response.data)
        self.assertEqual(result_child_child_comment['comment'], child_child_comment.comment, response.data)

    def test_create(self):
        article = ArticleFactory()

        url = reverse_lazy('blog:comments_list', kwargs=dict(pk=article.id))
        data = {
            'comment': 'comment',
            'parent': None,
        }
        response = self.client.post(url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['comment'], ArticleComment.objects.filter(pk=article.id).first().comment, response.data)


class CommentViewTest(WithLoginTestCase):

    def test_retrieve(self):
        comment = ArticleCommentFactory()
        child_comment = ArticleCommentFactory(parent=comment)
        child_child_comment = ArticleCommentFactory(parent=child_comment)

        url = reverse_lazy('blog:comment', kwargs=dict(pk=child_comment.pk))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data['id'], child_comment.pk, response.data)
