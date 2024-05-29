from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import BookTicketSerializer, EventSerializer, EventCreateSerializer, BookingSerializer
from .models import Event, Booking
import math
from decimal import Decimal

# SWAGGER
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# GOOGLE GEOCODING API
# import googlemaps

import jwt
import os
from dotenv import load_dotenv
load_dotenv()

# Create your views here.


@swagger_auto_schema(
    method='get',
    responses={200: EventSerializer(many=True)}
)
@swagger_auto_schema(
    method='post',
    request_body=EventCreateSerializer,
    responses={201: openapi.Response(
        'Event successfully created'), 400: 'Bad Request'}
)
@api_view(['GET', 'POST'])
def get_events(request):
    try:
        if request.method == 'GET':
            events = Event.objects.all()
            serializer = EventSerializer(events, many=True)
            Booking.objects.all().delete()
            Event.objects.all()

            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        if request.method == 'POST':
            # CHECK 1: ADMIN ONLY
            authorization_header = request.headers.get('Authorization')
            if authorization_header == None:
                return Response('No Authorization token found. Go to "http://127.0.0.1:8000/users/auth/create/" to get an auth token', status=status.HTTP_401_UNAUTHORIZED)
            token = authorization_header.split(' ')[1]

            # CHECK-2 ONLY ADMINS
            decode = jwt.decode(token, os.environ.get(
                'JWT_SECRET_KEY'), algorithms=['HS256'])
            if decode['is_admin'] is not True:
                return Response('Only Admins can create events', status=status.HTTP_400_BAD_REQUEST)

            serializer = EventCreateSerializer(data=request.data)
            if serializer.is_valid():
                event_name = serializer.validated_data['event_name']
                ticket_price = serializer.validated_data['ticket_price']
                total_tickets = serializer.validated_data['total_tickets']
                available_tickets = serializer.validated_data['available_tickets']
                date_of_event = serializer.validated_data['date_of_event']

                # GOOGLE GEOCODING to calculate LAT, LONG
                # ---------------------------------------
                # loc = serializer.validated_data['location']
                # gmaps = googlemaps.Client(key = os.environ.get('GOOGLE_MAPS_API_KEY'))
                # geocode_result = gmaps.geocode(loc)
                # print('🔥', geocode_result)

                Event.objects.create(event_name=event_name, ticket_price=ticket_price, total_tickets=total_tickets,
                                     available_tickets=available_tickets, date_of_event=date_of_event)
                return Response({'message': 'Event successfully created'}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method='get',
    responses={200: EventSerializer(), 404: 'Not Found'}
)
@api_view(['GET'])
def get_single_events(request, id):
    try:
        if request.method == 'GET':
            event = Event.objects.get(id=id)
            serializer = EventSerializer(event)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method='post',
    request_body=BookTicketSerializer,
    responses={201: openapi.Response('Booking created'), 400: 'Bad Request'}
)
@api_view(['POST'])
def book_event(request, id):
    try:
        serializer = BookTicketSerializer(data=request.data)
        if serializer.is_valid():
            number_of_tickets = serializer.validated_data['number_of_tickets']
            event = Event.objects.get(id=id)
            surge = False

            # CHECK-1: PROCEED IF USER IS VALID AUTH
            authorization_header = request.headers.get('Authorization')
            if authorization_header == None:
                return Response('No Authorization token found. Go to "http://127.0.0.1:8000/users/auth/create/" to get an auth token', status=status.HTTP_401_UNAUTHORIZED)

            token = authorization_header.split(' ')[1]
            decode = jwt.decode(token, os.environ.get(
                'JWT_SECRET_KEY'), algorithms=['HS256'])

            # FEATURE 1: NO HOARDING
            booking = Booking.objects.filter(
                email=decode['email'], event_name=event.event_name)
            if len(booking) != 0:
                return Response({'message': 'You cannot create multiple booking under same name'}, status=status.HTTP_400_BAD_REQUEST)

            print('🔥', type(event.available_tickets), type(
                number_of_tickets), event.available_tickets >= number_of_tickets)
            # CHECK-2:
            if event.available_tickets < number_of_tickets:
                return Response('Tickets not available. You have asked for more tickets than are available', status=status.HTTP_400_BAD_REQUEST)

            # DECREASE COUNT IN EVENTS TABLE
            event.available_tickets = event.available_tickets - number_of_tickets

            # CALCULATE TOTAL COST OF BOOKING
            cost = number_of_tickets * event.ticket_price
            if event.available_tickets <= math.floor(0.2*event.total_tickets):
                # FEATURE 2: SURGE PRICE
                cost = cost * Decimal(1.2)
                surge = True

            # ENTER IN BOOKING ENTRY
            booking = Booking.objects.create(email=decode['email'], phone=decode['phone'], event_name=event.event_name,
                                             ticket_price_paid=cost, tickets_purchased=number_of_tickets, surge_price_paid=surge)
            # ATOMIC BEHAVIOR
            event.save()

            return Response({'message': 'Booking created'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method='get',
    responses={200: BookingSerializer(many=True)}
)
@api_view(['GET'])
def my_bookings(request):
    try:
        if request.method == 'GET':
            events = Booking.objects.all()
            serializer = BookingSerializer(events, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
