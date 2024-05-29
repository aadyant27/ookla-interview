from django.urls import path
from . import views
urlpatterns = [
    path("", views.get_users, name='list-users'),
    path("create/", views.create_user, name='create-users'),
    path("auth/create/", views.create_token, name='create-auth-token')
]
