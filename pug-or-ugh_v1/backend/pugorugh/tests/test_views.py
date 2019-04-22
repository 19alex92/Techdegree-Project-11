from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate
from django.test import TestCase
from django.contrib.auth.models import User

from pugorugh.models import Dog, UserDog
from pugorugh.views import NextDogView, UpdateDogView, RetrieveUpdateUserPref


class TestNextDogView(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = NextDogView.as_view()
        self.user = User.objects.create(username='Testuser')

        self.dog = Dog.objects.create(
            name='TestDog1',
            image_filename='1.jpg',
            breed='testbreed',
            age=1,
            gender='m',
            size='l'
        )

    def test_get_single_dog_valid(self):
        request = self.factory.get('next-dog')
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=self.dog.pk, type='undecided')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_dog_invalid_no_auth(self):
        request = self.factory.get('next-dog')
        response = self.view(request, pk=self.dog.pk, type='undecided')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestUpdateDogView(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = UpdateDogView.as_view()
        self.user = User.objects.create(username='Testuser')
        self.dog = Dog.objects.create(
            name='TestDog1',
            image_filename='1.jpg',
            breed='testbreed',
            age=1,
            gender='m',
            size='l'
        )
        self.user_dog = UserDog.objects.create(
            user=self.user,
            dog=self.dog
        )
        self.request = self.factory.put('update-dog')

    def test_update_dog_status_valid(self):
        force_authenticate(self.request, user=self.user)
        response = self.view(self.request, pk=self.dog.pk, type='liked')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_dog_status_invalid_not_auth(self):
        response = self.view(self.request, pk=self.dog.pk, type='liked')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestRetrieveUpdateUserPrefView(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = RetrieveUpdateUserPref.as_view()
        self.user = User.objects.create(username='Testuser')

    def test_get_user_pref_valid(self):
        request = self.factory.get('user-prefs')
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_pref_invalid_no_auth(self):
        request = self.factory.get('user-prefs')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_pref_valid(self):
        request = self.factory.put('user-prefs', data=dict(
            age='a',
            gender='m',
            size='l'
        ))
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_pref_invalid_no_auth(self):
        request = self.factory.put('user-prefs', data={
            'age': 'a',
            'gender': 'm',
            'size': 'l'
        })
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
