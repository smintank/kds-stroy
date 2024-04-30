from unittest import TestCase

from django.urls import reverse
from django.test import Client


class OrderCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('orders:create')

    def test_create_order(self):
        response = self.client.post(self.url, data={
            'first_name': 'John',
            'phone_number': '79181089555',
            'city': 'Сочи'
        })
        self.assertEqual(response.status_code, 201)
