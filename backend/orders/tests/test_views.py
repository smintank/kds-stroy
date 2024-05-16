from django.test import TestCase

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.test import Client

from kds_stroy.settings import (
    MAX_UPLOADED_PHOTO_SIZE as PHOTO_SIZE
)
from orders.messages import ERROR_ORDER_CREATION_MSG
from orders.models import OrderPhoto

MByte = 1024 * 1024


def get_test_photos(data: bytes,
                    size=int(PHOTO_SIZE / 10)) -> SimpleUploadedFile:
    return SimpleUploadedFile(
        'test.jpg', data * (size * MByte), content_type='image/jpeg'
    )


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

        self.correct_photo = get_test_photos(b'A')
        self.big_photo = get_test_photos(b'F', PHOTO_SIZE + 1)
        self.empty_photo = get_test_photos(b'')
        self.not_photo = SimpleUploadedFile(
            'not_photo.txt', b'Text', content_type='txt/plain'
        )

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
                         {'error': ERROR_ORDER_CREATION_MSG})

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
            **{f'photo-{i}': get_test_photos(b'A', i) for i in range(1, 7)}
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(OrderPhoto.objects.count(), 5)

    def test_create_order_with_some_photos(self):
        response = self.client.post(self.url, {
            'first_name': self.first_name,
            'phone_number': self.phone_number,
            **{'photo-0': get_test_photos(b'A'),
               'photo-1': get_test_photos(b'B'),
               'photo-2': get_test_photos(b'C')}
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(OrderPhoto.objects.count(), 3)

    def test_create_order_with_valid_and_invalid_photos(self):
        response = self.client.post(self.url, {
            'first_name': self.first_name,
            'phone_number': self.phone_number,
            **{'photo-0': self.not_photo,
               'photo-1': self.big_photo,
               'photo-2': self.correct_photo}
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(OrderPhoto.objects.count(), 1)

    def test_create_order_with_only_invalid_photos(self):
        response = self.client.post(self.url, {
            'first_name': self.first_name,
            'phone_number': self.phone_number,
            **{'photo-0': self.not_photo,
               'photo-1': self.big_photo,
               'photo-2': self.empty_photo}
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(OrderPhoto.objects.count(), 0)

    def test_create_order_with_same_photos(self):
        response = self.client.post(self.url, {
            'first_name': self.first_name,
            'phone_number': self.phone_number,
            **{'photo-0': get_test_photos(b'A'),
               'photo-1': get_test_photos(b'A'),
               'photo-2': get_test_photos(b'A')}
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(OrderPhoto.objects.count(), 1)
