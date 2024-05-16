from django.test import Client, TestCase
from django.urls import reverse

from orders.models import City, Order, OrderPhoto


class OrderModelTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('orders:create')
        self.first_name = 'Client'
        self.phone_number = '79999999999'
        self.city = City.objects.filter(name='Сочи').first()
        self.address = 'ул. Ленина, д. 1'
        self.correct_comment = 'Comment'
        self.unsafe_comment = '_*`['

        self.order = Order.objects.create(
            first_name=self.first_name,
            phone_number=self.phone_number,
            city=self.city,
            address=self.address,
            comment=self.correct_comment
        )

    def test_order_creation(self):
        self.assertEqual(self.order.first_name, self.first_name)
        self.assertEqual(self.order.phone_number, self.phone_number)
        self.assertEqual(self.order.city, self.city)
        self.assertEqual(self.order.address, self.address)
        self.assertEqual(self.order.comment, self.correct_comment)
        self.assertEqual(self.order.status, Order.Status.REGISTERED)
        self.assertEqual(self.order.cost, 0.0)
        self.assertEqual(self.order.final_cost, 0.0)
        self.assertEqual(self.order.discount, 0)

    def test_order_minimal_creation(self):
        minimal_order = Order.objects.create(
            first_name=self.first_name,
            phone_number=self.phone_number
        )
        self.assertEqual(minimal_order.first_name, self.first_name)
        self.assertEqual(minimal_order.phone_number, self.phone_number)
        self.assertEqual(minimal_order.city, None)
        self.assertEqual(minimal_order.address, None)
        self.assertEqual(minimal_order.comment, None)
        self.assertEqual(minimal_order.status, Order.Status.REGISTERED)
        self.assertEqual(minimal_order.cost, 0.0)
        self.assertEqual(minimal_order.final_cost, 0.0)
        self.assertEqual(minimal_order.discount, 0)

    def test_order_str(self):
        self.assertEqual(str(self.order), f"Заказ №{self.order.order_id}")


class OrderPhotoModelTest(TestCase):
    def setUp(self):
        self.order = Order.objects.create(
            first_name="Client", phone_number="79999999999"
        )
        self.photo = OrderPhoto.objects.create(
            order=self.order,
            photo="correct1.jpg")

    def test_order_photo_creation(self):
        self.assertEqual(f"{self.photo.photo}", "correct1.jpg")
