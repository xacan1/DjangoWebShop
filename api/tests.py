from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from shop.models import *


class AttributesAPITest(APITestCase):
    def test_get(self):
        attribute1 = Attribute.objects.create(
            name='Аттрибут1', external_code='001')
        attribute2 = Attribute.objects.create(
            name='Аттрибут2', external_code='002')
        url = 'api/v1/attributes'
       
        response = self.client.get(url)
        print(response)
