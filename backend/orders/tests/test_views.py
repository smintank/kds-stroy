import os
from unittest import TestCase

from django.conf import settings
from django.urls import reverse
from django.test import Client

from orders.models import OrderPhoto


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
        self.data_dir = os.path.join(settings.BASE_DIR, 'orders/tests/data')

        self.not_photo = open(os.path.join(self.data_dir, 'test.txt'), 'rb')
        self.big_photo = open(os.path.join(self.data_dir, 'big.jpg'), 'rb')
        self.empty_photo = open(os.path.join(self.data_dir, 'empty.jpg'), 'rb')
        self.incorrect_photo = open(os.path.join(self.data_dir, 'incorrect.jpg'), 'rb')

        self.correct_photos = [
            open(os.path.join(self.data_dir, f'correct{i}.jpg'), 'rb')
            for i in range(1, 7)
        ]

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
        self.assertEqual(response.json(),
                         {'error': 'Не получилось создать заявку'})

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

    def test_create_order_with_more_than_5_photos(self):
        response = self.client.post(self.url, {
            'first_name': self.first_name,
            'phone_number': self.phone_number,
            'files': self.correct_photos
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(OrderPhoto.objects.count(), 5)

    def test_create_order_minimal_with_some_photos(self):
        photo_amount = 2
        response = self.client.post(self.url, {
            'first_name': self.first_name,
            'phone_number': self.phone_number,
            'files': self.correct_photos[0:photo_amount],
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(OrderPhoto.objects.count(), photo_amount)

    def test_create_order_minimal_with_all_invalid_photos(self):
        response = self.client.post(self.url, {
            'first_name': self.first_name,
            'phone_number': self.phone_number,
            'files': [self.correct_photos[0], self.incorrect_photo,
                      self.not_photo, self.empty_photo, self.big_photo],
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(OrderPhoto.objects.count(), 1)

    def test_create_order_with_same_photos(self):
        response = self.client.post(self.url, {
            'first_name': self.first_name,
            'phone_number': self.phone_number,
            'files': [
                self.correct_photos[2], self.correct_photos[2]
            ]
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(OrderPhoto.objects.count(), 1)



    def tearDown(self):
        OrderPhoto.objects.all().delete()
        # self.correct_photo.close()
        # self.not_photo.close()
        # self.big_photo.close()
        # self.empty_photo.close()
        # self.incorrect_photo.close()
        # for photo in self.correct_photos:
        #     photo.close()
