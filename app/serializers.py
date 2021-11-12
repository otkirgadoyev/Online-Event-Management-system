from .models import Organizator, Event, Participant, Notification
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class RegisterOrganizatorSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(label='Confirm Password',write_only=True)

    class Meta:
        model = Organizator
        fields = ('id','username','password','password2','fullname','email','phone')
        write_only_fields=('password','fullname','email','phone','password2')
        extra_kwargs = {
            'password' : {'write_only': True},
            'password2': {'write_only': True},
        }

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.pop('password2')
        if password != confirm_password:
            raise ValidationError('Passwords must match')
        return data

        
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class RegisterParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields=('id', 'fullname','email','phone','event')

    def to_representation(self, obj):
        return {
            "user": obj
        }

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields=('event','participant','is_send')

