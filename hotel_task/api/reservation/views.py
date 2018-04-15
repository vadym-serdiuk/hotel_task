from rest_framework import generics
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin

from hotel_task.api.reservation.serializers import ReservationSerializer
from hotel_task.models import Guest, Reservation


class ReservationViewSet(ViewSetMixin, generics.ListCreateAPIView):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()

    def create(self, request, *args, **kwargs):
        """
        Add new reservation.
        Returns 400 error if reservation is not possible for the date range

        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = dict(serializer.validated_data)
        guest = data.pop('guest')
        guest, _ = Guest.objects.get_or_create(**guest)

        reservation = Reservation.create_reservation(guest, **data)
        serializer = self.serializer_class(instance=reservation)

        return Response(serializer.data, 201)

    def list(self, request, *args, **kwargs):
        """
        Get list of reservations
        """
        return super().list(request, *args, **kwargs)
