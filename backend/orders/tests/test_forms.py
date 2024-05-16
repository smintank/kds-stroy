from unittest import TestCase

from orders.forms import OrderCreationForm
from orders.messages import (
    PHONE_MIN_LENGTH_ERROR_MSG,
    PHONE_MAX_LENGTH_ERROR_MSG
)


class FormTestCase(TestCase):
    def setUp(self):
        self.first_name = 'Name'
        self.phone_number = '79999999999'
        self.data = {
            'first_name': self.first_name,
            'phone_number': self.phone_number
        }

    def test_contact_form_valid(self):
        form = OrderCreationForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_contact_empty_form(self):
        form = OrderCreationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)
        self.assertEqual(form.errors['first_name'], ['Обязательное поле.'])
        self.assertEqual(form.errors['phone_number'], ['Обязательное поле.'])

    def test_contact_form_min_length_phone(self):
        form = OrderCreationForm(data={
            'first_name': self.first_name,
            'phone_number': '7999999999'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(form.errors['phone_number'],
                         [PHONE_MIN_LENGTH_ERROR_MSG])

    def test_contact_form_max_length_phone(self):
        form = OrderCreationForm(data={
            'first_name': self.first_name,
            'phone_number': '799999999999999'
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(form.errors['phone_number'],
                         [PHONE_MAX_LENGTH_ERROR_MSG])

    def test_contact_form_invalid_phone(self):
        form = OrderCreationForm(data={
            'first_name': self.first_name,
            'phone_number': '+$phone234'
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(form.errors['phone_number'],
                         [PHONE_MIN_LENGTH_ERROR_MSG])
