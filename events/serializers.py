from rest_framework import serializers
from .models import Event, Booking


class BookTicketSerializer(serializers.Serializer):
    number_of_tickets = serializers.IntegerField(min_value=1, max_value=4)


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class EventCreateSerializer(serializers.Serializer):
    event_name = serializers.CharField(max_length=255)
    ticket_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_tickets = serializers.IntegerField(min_value=10)
    available_tickets = serializers.IntegerField(min_value=1)  # TODO:
    date_of_event = serializers.DateTimeField()
    location = serializers.CharField(max_length=255)

    def validate(self, data):
        if data['available_tickets'] > data['total_tickets']:
            raise serializers.ValidationError(
                "Available tickets cannot exceed total tickets.")
        return data
