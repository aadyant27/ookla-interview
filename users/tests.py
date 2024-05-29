from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
import jwt
import os
from .models import User


class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email='testuser@example.com',
            phone='1234567890',
            is_admin=False
        )

    def test_get_users_empty(self):
        User.objects.all().delete()
        response = self.client.get(reverse('list-users'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_get_users_with_users(self):
        response = self.client.get(reverse('list-users'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['email'], 'testuser@example.com')

    def test_create_user_valid(self):
        valid_data = {
            'email': 'newuser@example.com',
            'phone': '0987654321',
            'is_admin': False
        }
        response = self.client.post(
            reverse('create-users'), valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_create_user_invalid(self):
        invalid_data = {
            'email': '',
            'password': 'newpassword',
            'phone': '0987654321',
            'is_admin': False
        }
        response = self.client.post(
            reverse('create-users'), invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_create_token_valid(self):
        valid_data = {'email': 'testuser@example.com'}
        response = self.client.post(
            reverse('create-auth-token'), valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('JWT token', response.data)

    def test_create_token_invalid_email(self):
        invalid_data = {'email': 'invalidemail@example.com'}
        response = self.client.post(
            reverse('create-auth-token'), invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'User does not exist')

    def test_create_token_invalid_data(self):
        invalid_data = {'email': ''}
        response = self.client.post(
            reverse('create-auth-token'), invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
