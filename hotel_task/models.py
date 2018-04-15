import datetime

from django.db import models
from django.db.models import Count, Max


class Guest(models.Model):
    """
    Model is used to store guests' info
    """
    name = models.CharField(max_length=200)
    email = models.EmailField()

    class Meta:
        unique_together = ('name', 'email')


class Reservation(models.Model):
    """
    Model is used to store guests' reservations
    """
    date = models.DateField()
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)

    @staticmethod
    def create_reservation(guest, date_start, date_end):
        dates = Reservation.get_dates_by_range(date_start, date_end)
        for date in dates:
            Reservation.objects.create(date=date, guest=guest)

    @staticmethod
    def get_dates_by_range(date_start, date_end):
        date = date_start
        dates = []
        while date < date_end:
            dates.append(date)
            date += datetime.timedelta(days=1)
        return dates

    @staticmethod
    def get_max_guests_for_dates(date_start, date_end):
        # we need not check the day of checkout
        date_end += datetime.timedelta(days=-1)
        reservations = (
            Reservation.objects
            .filter(date__range=(date_start, date_end))
            .values('date')
            .annotate(guests_number=Count('guest'))
            .aggregate(max_guests_number=Max('guests_number'))
        )

        return reservations['max_guests_number'] or 0


class Config(models.Model):
    """
    Model is used to store history of parameter values
    """
    PARAMETERS = {
        'overbooking': ('int', int, 100),
        'room_numbers': ('int', int, 3),
    }

    parameter = models.CharField(max_length=100)
    value = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_parameter_value(cls, name):
        assert name in cls.PARAMETERS

        parameter_options = cls.PARAMETERS.get(name)
        converter = parameter_options[1]

        param_object = Config.objects.filter(parameter=name).only('value').latest()
        return converter(param_object.value)


    class Meta:
        get_latest_by = 'date'


def load_initial_parameters(*args, **kwargs):
    """
    Initialize parameters in DB
    Used in post_migrate signal.
    Signal is connected in hotel_task.app.HotelTaskConfig class
    """
    for parameter, options in Config.PARAMETERS.items():
        default_value = options[2]
        if not Config.objects.filter(parameter=parameter).exists():
            Config.objects.create(parameter=parameter,
                                  value=default_value)
