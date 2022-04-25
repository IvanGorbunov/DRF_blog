from django.db import transaction
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from blog.models import Article, ArticleComment, User


class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = (
            'id',
            'title',
            'author'
        )


class ArticleDetailSerializer(serializers.ModelSerializer):
    comments_count = serializers.IntegerField(label='Количество комментариев')

    class Meta:
        model = Article
        fields = (
            'id',
            'title',
            'author',

            'create_dt',
            'change_dt',

            'comments_count',
        )


class ChangeUserMixin(serializers.Serializer):

    def validate(self, attrs):
        return super().validate(attrs)

    def get_request_user(self):
        return self.context['request'].user


class AuthorMixin(ChangeUserMixin):

    def validate(self, attrs):
        attrs.update({"author": self.get_request_user()})
        return super().validate(attrs)


class ArticleCreateEditSerializer(AuthorMixin, serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = (
            'id',
            'title',
        )

    @transaction.atomic()
    def create(self, validated_data):
        return super().create(validated_data)

    @transaction.atomic()
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class CommonFullUserSerializer(serializers.ModelSerializer):
    # first_name = serializers.CharField(source='get_first_name')
    # last_name = serializers.CharField(source='get_last_name')

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
        )


class RecursiveField(serializers.Serializer):
    """
    Поле для рекурсивного вывода дерева
    """

    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        return self.parent.parent.__class__(value, context=self.context).data


class ArticleCommentSerializer(serializers.ModelSerializer):
    user = CommonFullUserSerializer()
    comments = RecursiveField(many=True, required=False)

    class Meta:
        model = ArticleComment
        fields = (
            'id',
            'comment',
            'create_dt',
            'parent_id',
            # 'article',
            'user',
            'comments',
        )


class ArticleCommentCreateSerializer(serializers.ModelSerializer):
    create_dt = serializers.DateTimeField(read_only=True)
    # user = CommonFullUserSerializer(read_only=True)

    class Meta:
        model = ArticleComment
        fields = (
            'id',
            'comment',
            'parent',
            # 'article',
            'create_dt',
            # 'user',
        )

    def validate(self, attrs):
        article = get_object_or_404(Article, pk=self.context['request'].parser_context['kwargs']['pk'])
        parent = attrs.get('parent')
        if parent and parent.article_id != article.id:
            raise serializers.ValidationError(dict(parent='Статья родителя отличается'))
        attrs.update(
            dict(
                user=self.context['request'].user,
                article=article,
            )
        )
        return super().validate(attrs)


class ArticleCommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleComment
        fields = (
            'comment',
        )

