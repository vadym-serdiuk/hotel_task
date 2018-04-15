from rest_framework.decorators import api_view
from rest_framework.response import Response

from hotel_task.api.reservation.serializers import ReservationSerializer
from hotel_task.models import Guest, Reservation


@api_view(['POST'])
def reservation(request):
    serializer = ReservationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    data = dict(serializer.validated_data)
    guest = data.pop('guest')
    guest, _ = Guest.objects.get_or_create(**guest)

    Reservation.create_reservation(guest, **data)

    return Response(serializer.data, 201)
