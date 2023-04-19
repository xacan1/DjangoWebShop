from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework import status
from django.urls import reverse
from shop.models import *
from api.views import *
from api.serializers import *


class APITest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        set_requests_detail = {'get': 'retrieve',
                               'put': 'update',
                               'patch': 'partial_update',
                               'delete': 'destroy'}
        set_requests_list = {'get': 'list',
                             'post': 'create'}
        self.view_attribute_detail = AttributeAPIViewSet.as_view(
            set_requests_detail)
        self.view_attribute_list = AttributeAPIViewSet.as_view(set_requests_list)
        self.view_category_detail = CategoryAPIViewSet.as_view(set_requests_detail)
        self.view_category_list = CategoryAPIViewSet.as_view(set_requests_list)
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
        attr_test = {'name': 'Атрибут_Тест', 'external_code': '000001'}
        request = self.factory.post(url, attr_test, format='json')
        force_authenticate(request, user=self.test_admin)
        response = self.view_attribute_list(request)
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
        attr_test = {'name': 'Атрибут_Тест', 'external_code': '000001'}
        attr = Attribute.objects.create(**attr_test)
        new_name = 'Новое имя'
        url = reverse('attribute-detail', kwargs={'pk': attr.pk})
        request = self.factory.patch(url, {'name': new_name}, format='json')
        force_authenticate(request, user=self.test_admin)
        response = self.view_attribute_detail(request, pk=1)
        self.assertEqual(response.data['name'], new_name)

    # def test_category_create(self):
    #     url = reverse('Category-list')
    #     print(url)
    #     category_test = {'name': 'Категория_Тест', 'external_code': '000001'}
    #     request = self.factory.post(url, category_test, format='json')
    #     force_authenticate(request, user=self.test_admin)
    #     response = self.view_category_list(request)
    #     self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_category_list(self):
        cat1 = Category.objects.create(name='Категория_Тест1', external_code='001')
        cat2 = Category.objects.create(name='Категория_Тест2', external_code='002')
        url = reverse('Category-list')
        self.client.force_login(user=self.test_user)
        response = self.client.get(url)
        self.client.logout()
        serializer_data = CategorySerializer([cat1, cat2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_category_update(self):
        category_test = {'name': 'Категория_Тест', 'external_code': '000001'}
        cat = Category.objects.create(**category_test)
        new_name = 'Новое имя'
        url = reverse('Category-detail', kwargs={'pk': cat.pk})
        request = self.factory.patch(url, {'name': new_name}, format='json')
        force_authenticate(request, user=self.test_admin)
        response = self.view_category_detail(request, pk=1)
        self.assertEqual(response.data['name'], new_name)

"""
v=DKIM1;h=sha256;k=rsa;p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDFjStEOdAvrP6Y8Aa2cxmTzCKSbHlWzCr5esLOeYlcErVV4H9gDRf9TccTc60iifq8Z/D2vYAfsw8+CEU8rkJcYSfDUH4NRXZGA7x5BuNhQX0e8cqCuCpBxNDm4SRcq/dBXCbJqDZH/cFUVjx2mm8eKrugsiSXVty5dq+ztVS8XQIDAQAB
"""