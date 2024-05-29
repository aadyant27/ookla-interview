from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
import jwt
import os

from .models import Event, Booking
from .serializers import EventCreateSerializer, BookTicketSerializer


class EventTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_token = self.get_admin_token()

    def get_admin_token(self):
        return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFiaGlzaGVrQGdtYWlsLmNvbSIsInBob25lIjoiODA5MDAxMTQ0NCIsImlzX2FkbWluIjp0cnVlfQ.Y6G4cvq6sJNUexlyQaaT0TDHB22auzpx3CxaCvSlYL0"

    def test_get_events(self):
        response = self.client.get(reverse('list-create-events'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_event_invalid(self):
        valid_data = {
            'event_name': 'Test Event',
            'ticket_price': 10.0,
            'total_tickets': 100,
            'available_tickets': 100,
            'date_of_event': '2024-06-01'  # Date Invalid format | Location missing
        }
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        response = self.client.post(
            reverse('list-create-events'), valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_event_valid(self):
        valid_data = {
            'event_name': 'Test Event',
            'ticket_price': 10.0,
            'total_tickets': 100,
            'available_tickets': 100,
            'location': 'Bangalore',
            'date_of_event': '2024-06-30T14:30:00'  # Date is in valid format here
        }
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        response = self.client.post(
            reverse('list-create-events'), valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class BookingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_token = self.get_user_token()

    def get_user_token(self):
        return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFiaGlzaGVrQGdtYWlsLmNvbSIsInBob25lIjoiODA5MDAxMTQ0NCIsImlzX2FkbWluIjp0cnVlfQ.Y6G4cvq6sJNUexlyQaaT0TDHB22auzpx3CxaCvSlYL0"

    def test_book_event_valid(self):
        event = Event.objects.create(event_name='Test Event', ticket_price=10.0,
                                     total_tickets=100, available_tickets=100, date_of_event='2024-06-01')
        valid_data = {
            'number_of_tickets': 2
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        response = self.client.post(
            reverse('book-event', args=[event.id]), valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_book_event_invalid(self):
        event = Event.objects.create(event_name='Test Event', ticket_price=10.0,
                                     total_tickets=100, available_tickets=0, date_of_event='2024-06-01')
        invalid_data = {
            'number_of_tickets': 200
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        response = self.client.post(
            reverse('book-event', args=[event.id]), invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_my_bookings(self):
        # Create a booking for the user
        Booking.objects.create(email='testuser@example.com', phone='1234567890',
                               event_name='Test Event', ticket_price_paid=10.0, tickets_purchased=2)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        response = self.client.get(reverse('my-bookings'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
