from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Dog(models.Model):
    name = models.CharField(max_length=255)
    image_filename = models.CharField(max_length=255)
    breed = models.CharField(max_length=255, default='')
    age = models.IntegerField()
    gender = models.CharField(max_length=255, default='u')
    size = models.CharField(max_length=3, default='u')

    def __str__(self):
        return f"Name: {self.name} Id: {self.id}"


class UserDog(models.Model):
    # This model represents a link between a user and a dog

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, default='u')

    def __str__(self):
        return f"User: {self.user} Dog: {self.dog} USERDOG Pk: {self.pk}"


class UserPref(models.Model):
    # This model contains the user's preferences

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.CharField(max_length=10, default='b,y,a,s')
    gender = models.CharField(max_length=10, default='f,m')
    size = models.CharField(max_length=10, default='s,m,l,xl')


@receiver(post_save, sender=User)
def create_user_pref(sender, instance, created, **kwargs):
    # Creates UserPref + sets default UserDog status when registered
    if created:
        UserPref.objects.create(user=instance).save()
        for dog in Dog.objects.all():
            UserDog.objects.create(user=instance, dog=dog).save()
