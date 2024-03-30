from django.test import TestCase
from backend.orders.models import Order, OrderPhoto


class OrderModelTest(TestCase):
    def setUp(self):
        self.order = Order.objects.create(
            first_name='John',
            phone_number='1234567890',
            comment='test comment')

    def test_order_creation(self):
        self.assertEqual(f'{self.order.first_name}', 'John')
        self.assertEqual(f'{self.order.phone_number}', '1234567890')
        self.assertEqual(f'{self.order.comment}', 'test comment')
        self.assertEqual(f'{self.order.status}', 'Зарегистрирован')


class OrderPhotoModelTest(TestCase):
    def setUp(self):
        self.order = Order.objects.create(
            first_name='John',
            phone_number='1234567890',
            comment='test comment')
        self.photo = OrderPhoto.objects.create(
            order=self.order,
            photo='test.jpg'
        )

    def test_order_photo_creation(self):
        self.assertEqual(f'{self.photo.photo}', 'test.jpg')
