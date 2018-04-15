from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from hotel_task.models import Guest, Reservation, Config


class GuestSerializer(serializers.ModelSerializer):
    name = serializers.CharField(help_text='Name')
    class Meta:
        model = Guest
        fields = ('name', 'email')


class ReservationSerializer(serializers.Serializer):
    guest = GuestSerializer(help_text='''Guest json object as {"name": '', "email": ''}''')
    date_start = serializers.DateField(help_text="Date of arrival")
    date_end = serializers.DateField(help_text='Date of departure')

    def validate(self, attrs):

        overbooking = Config.get_parameter_value('overbooking')
        rooms_number = Config.get_parameter_value('rooms_number')
        if rooms_number == 0:
            raise ValidationError('Reservation forbidden', 403)

        max_guests_number = Reservation.get_max_guests_for_dates(
            attrs['date_start'], attrs['date_end']
        )
        if ((max_guests_number + 1) - rooms_number) / rooms_number * 100 > overbooking:
            raise ValidationError('Reservation limit exceeded for this date range', 400)

        return attrs
