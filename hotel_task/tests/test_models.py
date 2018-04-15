import datetime
import time

import pytest

from hotel_task.models import Guest, Reservation, Config


@pytest.mark.django_db
def test_guest_model():
    name = 'Test guest'
    email = 'test@mail.com'
    Guest.objects.create(name=name, email=email)
    guest  = Guest.objects.get(name=name)

    assert guest.name == name
    assert guest.email == email


@pytest.mark.django_db
def test_reservation_model():
    name = 'Test guest'
    email = 'test@mail.com'
    Guest.objects.create(name=name, email=email)
    guest  = Guest.objects.get(name=name)

    date = datetime.datetime(2018, 9, 1)
    reservation = Reservation.objects.create(guest=guest, date=date)

    assert reservation.guest == guest
    assert reservation.date == reservation.date


def test_dates_by_range1():
    """
    Test range in several days
    """
    date_start = datetime.datetime(2018, 4, 26)
    date_end = datetime.datetime(2018, 5, 5)
    dates = Reservation.get_dates_by_range(date_start, date_end)
    assert isinstance(dates, list)
    assert len(dates) == 9


def test_dates_by_range2():
    """
    Test range in 1 day
    """
    date_start = datetime.datetime(2018, 5, 1)
    date_end = datetime.datetime(2018, 5, 2)
    dates = Reservation.get_dates_by_range(date_start, date_end)
    assert isinstance(dates, list)
    assert len(dates) == 1


def test_dates_by_range3():
    """
    Testing bad range: date_start > date_end
    """
    format = '%Y-%m-%d'
    date_start = datetime.datetime(2018, 5, 1)
    date_end = datetime.datetime(2018, 4, 30)
    dates = Reservation.get_dates_by_range(date_start, date_end)
    assert isinstance(dates, list)
    assert len(dates) == 0


@pytest.mark.django_db
def test_create_reservation(guest):
    date_start = datetime.datetime(2018, 4, 26)
    date_end = datetime.datetime(2018, 5, 4)
    Reservation.create_reservation(guest, date_start, date_end)
    assert Reservation.objects.all().count() == 8


@pytest.mark.django_db
def test_max_guests_for_dates(reservations):
    # Checking the most loaded day
    date_start = datetime.datetime(2018, 4, 28)
    date_end = datetime.datetime(2018, 5, 3)
    max_guests_number = Reservation.get_max_guests_for_dates(date_start, date_end)
    assert max_guests_number == 3

    # Checking days out of reservation (should be 0)
    date_start = datetime.datetime(2018, 3, 1)
    date_end = datetime.datetime(2018, 3, 30)
    max_guests_number = Reservation.get_max_guests_for_dates(date_start, date_end)
    assert max_guests_number == 0

    # Checking the date on the end of reservation (should be 0)
    date_start = datetime.datetime(2018, 5, 29)
    date_end = datetime.datetime(2018, 5, 31)
    max_guests_number = Reservation.get_max_guests_for_dates(date_start, date_end)
    assert max_guests_number == 0

    # Checking the date on the beginning of reservation (should be 0)
    date_start = datetime.datetime(2018, 4, 20)
    date_end = datetime.datetime(2018, 4, 24)
    max_guests_number = Reservation.get_max_guests_for_dates(date_start, date_end)
    assert max_guests_number == 0


@pytest.mark.django_db
def test_config():
    parameter_name = 'overbooking'
    Config.objects.create(parameter=parameter_name, value='1')
    time.sleep(1)
    Config.objects.create(parameter=parameter_name, value='2')
    current_parameter_value = Config.get_parameter_value(parameter_name)
    assert current_parameter_value == 2
