from django.contrib.auth import get_user_model

from rest_framework import generics, permissions, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models
from . import serializers


class UserRegisterView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer


class RetrieveUpdateUserPref(generics.RetrieveUpdateAPIView):
    '''
        GET the UserPrefs
        PUT/Update the UserPrefs
    '''
    queryset = models.UserPref.objects.all()
    serializer_class = serializers.UserPrefSerializer

    def get_object(self):
        return models.UserPref.objects.filter(
            user__id__exact=self.request.user.id
            ).first()

    def put(self, request, *args, **kwargs):
        user_data = self.get_object()
        user_serializer = serializers.UserPrefSerializer(user_data,
                                                         request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data)
        return Response(user_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class UpdateDogView(APIView):
    '''Changes the status of the Dog'''

    def get_object(self):
        return models.UserDog.objects.filter(
            user__id=self.request.user.id,
            dog__id=self.kwargs.get('pk')
        ).first()

    def put(self, request, pk, type):
        updated_dog = self.get_object()
        updated_dog.status = type[0].lower()
        updated_dog.save()
        return Response(serializers.UserDogSerializer(updated_dog).data)


class NextDogView(generics.RetrieveAPIView):
    '''
        Gets the current UserPref from the User
        Filters the dogs by UserPrefs
        Filters the dogs by the UserDog status
        Provides one dog after another with the correct pks
    '''
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer

    def get_queryset(self):
        user = self.request.user
        prefs = models.UserPref.objects.get(user=user)

        pref_dogs = models.Dog.objects.filter(
            gender__in=prefs.gender.split(','),
            size__in=prefs.size.split(',')
        )

        rel_type = self.kwargs.get('type')
        return pref_dogs.filter(
            userdog__user__id=user.id,
            userdog__status=rel_type[0].lower()
        )

    def get_object(self):
        queryset = self.get_queryset()
        pk = self.kwargs.get('pk')

        dog = queryset.filter(id__gt=pk).first()

        if dog is not None:
            return dog
        return queryset.first()
