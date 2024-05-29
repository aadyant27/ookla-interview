from django.urls import path
from . import views
urlpatterns = [
    path("", views.get_events, name='list-create-events'),
    path("<int:id>/", views.get_single_events, name='get_single_events-event'),
    path("<int:id>/book/", views.book_event, name='book-event'),
    path("bookings/", views.my_bookings, name='my-bookings')
]
