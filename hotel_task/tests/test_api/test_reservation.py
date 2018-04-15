import pytest
from rest_framework.test import APIClient

from hotel_task.models import Reservation, Guest


@pytest.mark.django_db
class TestReservation:
    path = '/reservation/'

    def test_first_reservation(self, reservations):
        client = APIClient()
        data = {
            'guest': {
                'name': 'Test',
                'email': 'test@g.com',
            },
            'date_start': '2018-06-20',
            'date_end': '2018-06-21',
        }
        prev_guests_count = Guest.objects.count()
        prev_reservation_count = Reservation.objects.count()

        response = client.post(self.path, data=data, format='json')

        assert 201 == response.status_code
        assert prev_guests_count + 1 == Guest.objects.count()
        assert prev_reservation_count + 1 == Reservation.objects.count()

    def test_reservation_non_overbooked(self, reservations):
        client = APIClient()
        data = {
            'guest': {
                'name': 'Test',
                'email': 'test@g.com',
            },
            'date_start': '2018-05-20',
            'date_end': '2018-05-21',
        }
        prev_guests_count = Guest.objects.count()
        prev_reservation_count = Reservation.objects.count()

        response = client.post(self.path, data=data, format='json')

        assert 201 == response.status_code
        assert prev_guests_count + 1 == Guest.objects.count()
        assert prev_reservation_count + 1 == Reservation.objects.count()

    def test_reservation_overbooking_forbidden(self, reservations):
        client = APIClient()
        data = {
            'guest': {
                'name': 'Test',
                'email': 'test@g.com',
            },
            'date_start': '2018-05-02',
            'date_end': '2018-05-04',
        }
        prev_guests_count = Guest.objects.count()
        prev_reservation_count = Reservation.objects.count()

        response = client.post(self.path, data=data, format='json')

        assert 400 == response.status_code
        assert prev_guests_count == Guest.objects.count()
        assert prev_reservation_count == Reservation.objects.count()

    def test_reservation_overbooking_allowed(self, reservations):
        client = APIClient()
        data = {
            'guest': {
                'name': 'Test',
                'email': 'test@g.com',
            },
            'date_start': '2018-05-02',
            'date_end': '2018-05-04',
        }
        prev_guests_count = Guest.objects.count()
        prev_reservation_count = Reservation.objects.count()

        client.put('/config/overbooking/', {'value': '40'})

        response = client.post(self.path, data=data, format='json')

        assert 201 == response.status_code
        assert prev_guests_count + 1 == Guest.objects.count()
        assert prev_reservation_count + 2 == Reservation.objects.count()