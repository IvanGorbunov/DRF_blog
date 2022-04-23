from django.db import transaction
from rest_framework import serializers

from blog.models import Article


class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = (
            'id',
            'title',
            'author'
        )


class ArticleDetailSerializer(serializers.ModelSerializer):

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
        # attrs.update({"change_last_user": self.get_request_user()})
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
            # 'author',
        )

    @transaction.atomic()
    def create(self, validated_data):
        # user = self.get_request_user()

        return super().create(validated_data)

    @transaction.atomic()
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


