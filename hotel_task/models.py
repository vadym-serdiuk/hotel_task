from django.db import models
from django.db.models import signals
from django.dispatch import receiver

from hotel_task.app import HotelTaskConfig


class Guest(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()


class Reservation(models.Model):
    date = models.DateField()
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)


class Config(models.Model):
    PARAMETERS = {
        'overbooking': ('int', int, 100),
        'room_numbers': ('int', int, 3),
    }

    parameter = models.CharField(max_length=100)
    value = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = 'date'


def load_initial_parameters(*args, **kwargs):
    """
    Initialize parameters in DB
    """
    for parameter, options in Config.PARAMETERS.items():
        default_value = options[2]
        if not Config.objects.filter(parameter=parameter).exists():
            Config.objects.create(parameter=parameter,
                                  value=default_value)
