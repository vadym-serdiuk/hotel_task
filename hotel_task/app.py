from django.apps import AppConfig
from django.db.models import signals
from django.dispatch import Signal


class HotelTaskConfig(AppConfig):

    name = 'hotel_task'

    def ready(self):
        from hotel_task.models import load_initial_parameters

        Signal.connect(signals.post_migrate, receiver=load_initial_parameters, sender=self)
