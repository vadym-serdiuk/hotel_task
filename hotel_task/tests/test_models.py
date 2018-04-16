import datetime
import time

import pytest

from hotel_task.models import Guest, Reservation, Config, ReservationDates


@pytest.mark.django_db
def test_guest_model():
    name = 'Test guest'
    email = 'test@mail.com'
    Guest.objects.create(name=name, email=email)
    guest = Guest.objects.get(name=name)

    assert name == guest.name
    assert email == guest.email


@pytest.mark.django_db
def test_reservation_model():
    name = 'Test guest'
    email = 'test@mail.com'
    Guest.objects.create(name=name, email=email)
    guest = Guest.objects.get(name=name)

    date_start = datetime.date(2018, 9, 1)
    date_end = datetime.date(2018, 9, 10)
    reservation = Reservation.objects.create(
        guest=guest,
        date_start=date_start,
        date_end=date_end,
    )

    assert guest == reservation.guest
    assert date_start == reservation.date_start
    assert date_end == reservation.date_end

    assert 9 == ReservationDates.objects.count()


def test_dates_by_range1():
    """
    Test range in several days
    """
    date_start = datetime.date(2018, 4, 26)
    date_end = datetime.date(2018, 5, 5)
    dates = Reservation.get_dates_by_range(date_start, date_end)
    assert isinstance(dates, list)
    assert 9 == len(dates)


def test_dates_by_range2():
    """
    Test range in 1 day
    """
    date_start = datetime.date(2018, 5, 1)
    date_end = datetime.date(2018, 5, 2)
    dates = Reservation.get_dates_by_range(date_start, date_end)
    assert isinstance(dates, list)
    assert 1 == len(dates)


def test_dates_by_range3():
    """
    Testing bad range: date_start > date_end
    """
    date_start = datetime.date(2018, 5, 1)
    date_end = datetime.date(2018, 4, 30)
    dates = Reservation.get_dates_by_range(date_start, date_end)
    assert isinstance(dates, list)
    assert 0 == len(dates)


@pytest.mark.django_db
def test_create_reservation(guest):
    date_start = datetime.date(2018, 4, 26)
    date_end = datetime.date(2018, 5, 4)
    reservation = Reservation.create_reservation(guest, date_start, date_end)
    assert 8 == ReservationDates.objects.filter(reservation_id=reservation.id).count()


@pytest.mark.django_db
def test_max_guests_for_dates(reservations):
    # Checking the most loaded day
    date_start = datetime.date(2018, 4, 28)
    date_end = datetime.date(2018, 5, 3)
    max_guests_number = Reservation.get_max_guests_for_dates(date_start, date_end)
    assert 3 == max_guests_number

    # Checking days out of reservation (should be 0)
    date_start = datetime.date(2018, 3, 1)
    date_end = datetime.date(2018, 3, 30)
    max_guests_number = Reservation.get_max_guests_for_dates(date_start, date_end)
    assert 0 == max_guests_number

    # Checking the date on the end of reservation (should be 0)
    date_start = datetime.date(2018, 5, 29)
    date_end = datetime.date(2018, 5, 31)
    max_guests_number = Reservation.get_max_guests_for_dates(date_start, date_end)
    assert 0 == max_guests_number

    # Checking the date on the beginning of reservation (should be 0)
    date_start = datetime.date(2018, 4, 20)
    date_end = datetime.date(2018, 4, 24)
    max_guests_number = Reservation.get_max_guests_for_dates(date_start, date_end)
    assert 0 == max_guests_number


@pytest.mark.django_db
def test_config():
    parameter_name = 'overbooking'
    Config.objects.create(parameter=parameter_name, value='1')
    time.sleep(1)
    Config.objects.create(parameter=parameter_name, value='2')
    current_parameter_value = Config.get_parameter_value(parameter_name)
    assert 2 == current_parameter_value
