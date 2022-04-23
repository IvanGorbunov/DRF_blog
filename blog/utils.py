from django.db import models
from django.db.models import Q
from django_filters import CharFilter
from django_filters.rest_framework import FilterSet
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet

from django.test import override_settings
from rest_framework.test import APITestCase

from django.utils.timezone import now as tz_now


def generate_uniq_code():
    return str(tz_now().timestamp()).replace('.', '')


class CreateModelMixin(models.Model):
    create_dt = models.DateTimeField('Создание записи', auto_now_add=True)

    class Meta:
        abstract = True


class DateModelMixin(CreateModelMixin, models.Model):

    change_dt = models.DateTimeField('Изменение записи', auto_now=True)

    class Meta:
        abstract = True


class MultiSerializerViewSet(ModelViewSet):
    filtersets = {
        'default': None,
    }
    serializers = {
        'default': Serializer,
    }

    @property
    def filterset_class(self):
        return self.filtersets.get(self.action) or self.filtersets.get('default')

    @property
    def serializer_class(self):
        return self.serializers.get(self.action) or self.serializers.get('default', Serializer)

    def get_response(self, data=None):
        return Response(data)

    def get_valid_data(self, many=False):
        serializer = self.get_serializer(data=self.request.data, many=many)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data


@override_settings(SQL_DEBUG=False)
class TestCaseBase(APITestCase):
    """
    Базовый (без авторизации)
    """
    CONTENT_TYPE_JSON = 'application/json'

    def check_status(self, response, status):
        self.assertEqual(response.status_code, status, response.data)

    def generate_uniq_code(self):
        return generate_uniq_code()


class SearchFilterSet(FilterSet):
    search_fields = ()
    search_method = 'icontains'
    q = CharFilter(method='filter_search', help_text='Поиск')

    def filter_search(self, queryset, name, value):
        if value:
            q_objects = Q()
            for field in self.search_fields:
                q_objects |= Q(**{f'{field}__{self.search_method}': value})
            queryset = queryset.filter(q_objects)
        return queryset.distinct()
