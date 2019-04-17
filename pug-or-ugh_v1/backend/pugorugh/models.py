from django.contrib.auth.models import User
from django.db import models


class Dog(models.Model):
    name = models.CharField(max_length=255)
    image_filename = models.CharField(max_length=255)
    breed = models.CharField(max_length=255, default='')
    age = models.IntegerField()
    gender = models.CharField(max_length=255, default='u')
    size = models.CharField(max_length=3, default='u')

    def __str__(self):
        return self.name


class UserDog(models.Model):
    # This model represents a link between a user and a dog

    user = models.ForeignKey(User, related_name='user_dog_relation')
    dog = models.ForeignKey(User, related_name='dog_user_relation')
    status = models.CharField(max_length=1, default='')


class UserPref(models.Model):
    # This model contains the user's preferences

    user = models.ForeignKey(User, related_name='user_pref')
    age = models.CharField(max_length=255, default='')
    gender = models.CharField(max_length=255, default='')
    size = models.CharField(max_length=255, default='')
