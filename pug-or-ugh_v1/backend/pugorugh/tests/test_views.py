from rest_framework import status
from rest_framework.test import (APITestCase, APIRequestFactory,
                                 force_authenticate)
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy

from pugorugh.models import Dog, UserDog, UserPref
from pugorugh.views import NextDogView, UpdateDogView, RetrieveUpdateUserPref
from pugorugh.serializers import (DogSerializer, UserDogSerializer,
                                  UserPrefSerializer)


class TestNextDogView(APITestCase):
    ''' 
        Tests to get a get request, tests for correct
        response data as well as tests for auth
    '''

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
        UserDog.objects.create(
            user=self.user,
            dog=self.dog
        )

    def test_get_single_dog_valid(self):
        request = self.factory.get('next-dog')
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=self.dog.pk, type='undecided')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_dog_get_correct_response_data(self):
        request = self.factory.get('next_dog')
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=self.dog.pk, type='undecided')
        serializer = DogSerializer(Dog.objects.all(), many=True)
        expected_response = {'id': 1,
                             'name': 'TestDog1',
                             'image_filename': '1.jpg',
                             'breed': 'testbreed',
                             'age': 1,
                             'gender': 'm',
                             'size': 'l'}
        self.assertEqual(response.data, dict(serializer.data[0]))
        #  This test fails if one changes the model fields, serializer fiels
        #  and fails if the view isn't functioning properly
        self.assertEqual(response.data, expected_response)

    def test_get_single_dog_invalid_no_auth(self):
        request = self.factory.get('next-dog')
        response = self.view(request, pk=self.dog.pk, type='undecided')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestUpdateDogView(APITestCase):
    '''
        Tests to do a put request, tests for correct
        response data as well as tests for auth
    '''

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

    def test_update_dog_get_correct_response_data(self):
        request = self.factory.put('update-dog', kwargs={'pk': self.dog.pk, 'status': 'disliked'})
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=self.dog.pk, type='disliked')
        serializer = UserDogSerializer(UserDog.objects.filter(pk=self.dog.pk), many=True)
        expected_response = {'status': 'd'}
        self.assertEqual(response.data, dict(serializer.data[0]))
        #  This test fails if one changes the model fields, serializer fiels
        #  and fails if the view isn't functioning properly
        self.assertEqual(response.data, expected_response)

    def test_update_dog_status_invalid_not_auth(self):
        response = self.view(self.request, pk=self.dog.pk, type='liked')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestRetrieveUpdateUserPrefView(APITestCase):
    '''
        Tests to do a get and a put request, tests for correct
        response data as well as tests for auth
    '''

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = RetrieveUpdateUserPref.as_view()
        self.user = User.objects.create(username='Testuser')

    def test_get_user_pref_valid(self):
        request = self.factory.get('user-prefs')
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_get_correct_response_data(self):
        request = self.factory.get('user-prefs')
        force_authenticate(request, user=self.user)
        response = self.view(request)
        serializer = UserPrefSerializer(UserPref.objects.get())
        expected_response = {'age': 'b,y,a,s',
                             'gender': 'f,m',
                             'size': 's,m,l,xl'}
        self.assertEqual(response.data, serializer.data)
        #  This test fails if one changes the model fields
        #  or their default values, serializer fiels
        #  and fails if the view isn't functioning properly
        self.assertEqual(response.data, expected_response)

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

    def test_update_user_correct_response_data(self):
        request = self.factory.put('user-prefs', data=dict(
            age='a',
            gender='m',
            size='l'
        ))
        force_authenticate(request, user=self.user)
        response = self.view(request)
        serializer = UserPrefSerializer(UserPref.objects.get())
        expected_response = {'age': 'a', 'gender': 'm', 'size': 'l'}
        self.assertEqual(response.data, serializer.data)
        #  This test fails if one changes the model fields, serializer fiels
        #  and fails if the view isn't functioning properly
        self.assertEqual(response.data, expected_response)

    def test_update_user_pref_invalid_no_auth(self):
        request = self.factory.put('user-prefs', data={
            'age': 'a',
            'gender': 'm',
            'size': 'l'
        })
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
