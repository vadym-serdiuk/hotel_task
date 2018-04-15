import datetime

from django.contrib import admin
from django.db import models
from django.db.models import Count, Max


class Guest(models.Model):
    """
    Model is used to store guests' info
    """
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return '{} ({})'.format(self.name, self.email)

    class Meta:
        unique_together = ('name', 'email')


class Reservation(models.Model):
    """
    Model is used to store guests' reservations
    """
    date_start = models.DateField()
    date_end = models.DateField()
    guest = models.ForeignKey(Guest, on_delete=models.PROTECT)

    def __str__(self):
        return 'Guest: {}, dates: {}-'.format(self.guest, self.date_start, self.date_end)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save(force_insert=False, force_update=False, using=None,
                     update_fields=None)

        # Add calendar records
        dates = Reservation.get_dates_by_range(self.date_start, self.date_end)
        for date in dates:
            ReservationDates.objects.create(reservation_id=self.pk, date=date)

    @staticmethod
    def create_reservation(guest: Guest, date_start: datetime.date, date_end: datetime.date):
        return Reservation.objects.create(guest=guest, date_start=date_start, date_end=date_end)

    @staticmethod
    def get_dates_by_range(date_start: datetime.date, date_end: datetime.date) -> list:
        """
        Transforms date range to the list of dates
        :param date_start:
        :param date_end:
        :return: list
        """
        date = date_start
        dates = []
        while date < date_end:
            dates.append(date)
            date += datetime.timedelta(days=1)
        return dates

    @staticmethod
    def get_max_guests_for_dates(date_start: datetime.date, date_end: datetime.date) -> int:
        """
        Calculates max booked rooms in the range of dates
        :param date_start:
        :param date_end:
        :return: int
        """

        # we need not check the day of checkout
        date_end += datetime.timedelta(days=-1)

        reservations = (
            ReservationDates.objects
            .filter(date__range=(date_start, date_end))
            .values('date')
            .annotate(guests_number=Count('reservation'))
            .aggregate(max_guests_number=Max('guests_number'))
        )

        return reservations['max_guests_number'] or 0


class ReservationDates(models.Model):
    """
    Model to store reservation as expanded date range
    """
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    date = models.DateField()


class Config(models.Model):
    """
    Model is used to store history of parameter values
    """
    PARAMETERS = {
        'overbooking': ('int', int, 0),
        'rooms_number': ('int', int, 3),
    }

    parameter = models.CharField(max_length=100)
    value = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} at {}'.format(self.parameter, self.date)

    @classmethod
    def get_parameter_value(cls, name):
        assert name in cls.PARAMETERS

        parameter_options = cls.PARAMETERS.get(name)
        converter = parameter_options[1]

        param_object = Config.objects.filter(parameter=name).only('value').latest()
        return converter(param_object.value)

    class Meta:
        get_latest_by = ('date', 'id')


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


admin.site.register(Guest)
admin.site.register(Reservation)
admin.site.register(Config)
