import os
from unittest import TestCase

from django.conf import settings
from django.urls import reverse
from django.test import Client


class OrderCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('orders:create')
        self.first_name = 'Client'
        self.phone_number = '79999999999'
        self.city = 'Краснодарский край, г. Сочи'
        self.address = 'ул. Ленина, д. 1'
        self.correct_comment = 'Comment'
        self.unsafe_comment = '_*`['

        # photos
        test_dir = os.path.join(settings.BASE_DIR, 'orders/tests/data')

        self.correct_photo = open(os.path.join(test_dir, 'test.jpg'), 'rb')
        self.not_photo = open(os.path.join(test_dir, 'test.txt'), 'rb')
        self.big_photo = open(os.path.join(test_dir, 'big.jpg'), 'rb')
        self.empty_photo = open(os.path.join(test_dir, 'empty.jpg'), 'rb')
        self.incorrect_photo = open(os.path.join(test_dir, 'incorrect.jpg'), 'rb')

    def test_create_order_minimal(self):
        response = self.client.post(self.url, {
            'first_name': self.first_name,
            'phone_number': self.phone_number,
        })
        self.assertEqual(response.status_code, 201)

    def test_create_order_full(self):
        response = self.client.post(self.url, {
            'first_name': self.first_name,
            'phone_number': self.phone_number,
            'city': self.city,
            'address': self.address,
            'comment': self.correct_comment,
        })
        self.assertEqual(response.status_code, 201)

    def test_create_order_unsafe_comment(self):
        response = self.client.post(self.url, {
            'first_name': self.first_name,
            'phone_number': self.phone_number,
            'comment': self.unsafe_comment,
        })
        self.assertEqual(response.status_code, 201)

    def test_create_order_empty(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 400)

    def test_create_order_empty_first_name(self):
        response = self.client.post(self.url, {
            'phone_number': self.phone_number,
        })
        self.assertEqual(response.status_code, 400)

    def test_create_order_empty_phone_number(self):
        response = self.client.post(self.url, {
            'first_name': self.first_name,
        })
        self.assertEqual(response.status_code, 400)

    def test_create_order_minimal_with_correct_photo(self):
        response = self.client.post(self.url, {
            'first_name': self.first_name,
            'phone_number': self.phone_number,
            'files': self.correct_photo,
        })
        self.assertEqual(response.status_code, 201)

    def test_create_order_minimal_with_not_photo(self):
        response = self.client.post(self.url, {
            'first_name': self.first_name,
            'phone_number': self.phone_number,
            'files': self.not_photo,
        })
        self.assertEqual(response.status_code, 400)

    def test_create_order_minimal_with_big_photo(self):
        response = self.client.post(self.url, {
            'first_name': self.first_name,
            'phone_number': self.phone_number,
            'files': self.big_photo,
        })
        self.assertEqual(response.status_code, 400)

    def test_create_order_minimal_with_empty_photo(self):
        response = self.client.post(self.url, {
            'first_name': self.first_name,
            'phone_number': self.phone_number,
            'files': self.empty_photo,
        })
        self.assertEqual(response.status_code, 400)

    def test_create_order_minimal_with_incorrect_photo(self):
        response = self.client.post(self.url, {
            'first_name': self.first_name,
            'phone_number': self.phone_number,
            'files': self.incorrect_photo,
        })
        self.assertEqual(response.status_code, 400)

    def tearDown(self):
        self.correct_photo.close()
        self.not_photo.close()
        self.big_photo.close()
        self.empty_photo.close()
        self.incorrect_photo.close()
