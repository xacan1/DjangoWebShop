from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework import status
from django.urls import reverse
from shop.models import *
from api.views import *
from api.serializers import *


class AttributesAPITest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view_detail = AttributeAPIViewSet.as_view({'get': 'retrieve',
                                                        'put': 'update',
                                                        'patch': 'partial_update',
                                                        'delete': 'destroy'})
        self.view_list = AttributeAPIViewSet.as_view({'get': 'list',
                                                      'post': 'create'})
        self.attr_test = {'name': 'Атрибут_Тест', 'external_code': '000001'}
        self.test_user = User.objects.create(
            email='test@mail.ru',
            phone='1234567890',
            is_active=True
        )
        self.test_admin = User.objects.create(
            email='staff@mail.ru',
            phone='234567890',
            is_active=True,
            is_staff=True
        )

    def test_attribute_create(self):
        url = reverse('attribute-list')
        request = self.factory.post(url, self.attr_test, format='json')
        force_authenticate(request, user=self.test_admin)
        response = self.view_list(request)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_attribute_list(self):
        attr1 = Attribute.objects.create(name='Атрибут1', external_code='001')
        attr2 = Attribute.objects.create(name='Атрибут2', external_code='002')
        url = reverse('attribute-list')
        self.client.force_login(user=self.test_user)
        response = self.client.get(url)
        self.client.logout()
        serializer_data = AttributeSerializer([attr1, attr2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_attribute_update(self):
        attr = Attribute.objects.create(**self.attr_test)
        new_name = 'Новое имя'
        url = reverse('attribute-detail', kwargs={'pk': attr.pk})
        request = self.factory.patch(url, {'name': new_name}, format='json')
        force_authenticate(request, user=self.test_admin)
        response = self.view_detail(request, pk=1)
        self.assertEqual(response.data['name'], new_name)
