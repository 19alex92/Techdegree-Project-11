from django.contrib.auth.models import User
from django.test import TestCase

from pugorugh.models import Dog, UserDog, UserPref


class TestDogAndUserDogModel(TestCase):
    '''Tests creation of Dog and UserDog model'''
    def setUp(self):
        self.user = User.objects.create(
            first_name='TestUser',
            last_name='TestLastName',
            email='test@email.com',
            password='SuperSecret',
        )
        self.dog = Dog.objects.create(
            name='TestDog',
            image_filename='1.jpg',
            breed='testbreed',
            age=1,
            gender='m',
            size='l'
        )
        self.user_dog = UserDog.objects.create(
            user=self.user,
            dog=self.dog,
            status='u'
        )

    def test_dog_creation(self):
        dog = self.dog
        self.assertTrue(isinstance(dog, Dog))

    def test_user_dog_creation(self):
        user_dog = self.user_dog
        self.assertTrue(isinstance(user_dog, UserDog))


class TestUserPrefModel(TestCase):
    '''Tests creation of UserPref model'''
    def setUp(self):
        self.user = User.objects.create(
            first_name='TestUser',
            last_name='TestLastName',
            email='test@email.com',
            password='SuperSecret',
        )
        self.user_pref = UserPref.objects.create(
            user=self.user,
            age='a',
            gender='m',
            size='l'
        )

    def test_user_pref_creation(self):
        user_pref = self.user_pref
        self.assertTrue(isinstance(user_pref, UserPref))
