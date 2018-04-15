import datetime

import pytest

from hotel_task.models import Guest, Reservation


@pytest.fixture
def guest():
    name = 'Test guest'
    email = 'test@mail.com'
    return Guest.objects.create(name=name, email=email)


@pytest.fixture
def reservations(guest):
    reservations = (
        ((2018, 4, 24), (2018, 4, 29), ('Test1', 't1@g.com')),
        ((2018, 4, 27), (2018, 5, 3), ('Test2', 't2@g.com')),
        ((2018, 5, 1), (2018, 5, 10), ('Test3', 't3@g.com')),
        ((2018, 5, 2), (2018, 5, 3), ('Test4', 't4@g.com')),
        ((2018, 5, 3), (2018, 5, 6), ('Test5', 't5@g.com')),
        ((2018, 5, 7), (2018, 5, 29), ('Test6', 't6@g.com')),
    )

    for date_start, date_end, (name, email) in reservations:
        guest, _ = Guest.objects.get_or_create(name=name, email=email)
        reservation = Reservation.create_reservation(
            guest,
            datetime.datetime(*date_start),
            datetime.datetime(*date_end),
        )