from rest_framework.test import RequestsClient
from django.test import TestCase
from .models import *


client = RequestsClient()
response = client.get('http://127.0.0.1:8000/api/submit_data')
print("Method: check request 200")
assert response.status_code == 200

response = client.get('http://127.0.0.1:8000/api/submit_data/sakjhiasd')
print("Method: check request 404")
assert response.status_code == 404

response = client.get('http://127.0.0.1:8000/api/submit_data/250')
print("Method: check request 404")
assert response.status_code == 404

response = client.get('http://127.0.0.1:8000/api/submit_data/?user__email=example@gmail.com')
print("Method: check request 200")
assert response.status_code == 200


class PerevalTestCase(TestCase):
    coord_dict = {
        'latitude': 1.235,
        'longitude': 12.255,
        'height': 250
    }

    level_dict = {
        'winter': '1A',
        'summer': None,
        'autumn': '1A',
        'spring': '1A'
    }
    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")

        user = CustomUser.objects.create(
            email="test@gmail.com",
            fam="Family",
            name="Name",
            otc="Otchestvo",
            phone="+38021458654"
        )
        coords = Coords.objects.create(
            latitude=1.235,
            longitude=12.255,
            height=250
        )
        Pereval.objects.create(
            user=user,
            coords=coords,
            beauty_title='Beauty',
            title='Title',
            other_titles='Other',
            connect='Connect',
            winter='1A',
            summer=None,
            autumn='1A',
            spring='1A',
            status='pending',
        )

    def test_custom_user_true(self):
        print("Method: test_custom_user_true.")
        user = CustomUser.objects.get(email='test@gmail.com')
        same_email = CustomUser.objects.filter(email='test@gmail.com').count()
        self.assertEqual(user.get_fio(), 'Name Otchestvo Family')
        self.assertEqual(user.get_count_perevals(), 1)
        self.assertEqual(same_email, 1)

    def test_custom_user_false(self):
        print("Method: test_custom_user_false.")
        user = CustomUser.objects.get(email='test@gmail.com')
        same_email = CustomUser.objects.filter(email='test@gmail.com').count()
        self.assertFalse(user.get_fio(), 'Some Name')
        self.assertFalse(user.get_count_perevals(), 0)
        self.assertFalse(same_email, 0)

    def test_coords_true(self):
        print("Method: test_coords_true.")
        coord = Coords.objects.get(latitude=1.235, longitude=12.255, height=250)
        same_coord = Coords.objects.filter(latitude=1.235, longitude=12.255, height=250).count()
        self.assertEqual(coord.get_dict(), self.coord_dict)
        self.assertEqual(same_coord, 1)

    def test_coords_false(self):
        print("Method: test_coords_false.")
        coord = Coords.objects.get(latitude=1.235, longitude=12.255, height=250)
        same_coord = Coords.objects.filter(latitude=1.235, longitude=12.255, height=250).count()
        self.assertFalse(coord.get_dict(), {})
        self.assertFalse(same_coord, 0)

    def test_pereval_true(self):
        print("Method: test_pereval_true.")
        pereval = Pereval.objects.get(
            beauty_title='Beauty',
            title='Title',
            other_titles='Other',
            connect='Connect',
            winter='1A',
            summer=None,
            autumn='1A',
            spring='1A',
            status='pending'
        )

        self.assertEqual(pereval.get_level_dict(), self.level_dict)

    def test_pereval_false(self):
        print("Method: test_pereval_false.")
        pereval = Pereval.objects.get(
            beauty_title='Beauty',
            title='Title',
            other_titles='Other',
            connect='Connect',
            winter='1A',
            summer=None,
            autumn='1A',
            spring='1A',
            status='pending'
        )

        self.assertFalse(pereval.get_level_dict(), {})
