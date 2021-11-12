from django.db import models
from django.contrib.auth.models import AbstractUser



class Organizator(AbstractUser):
    fullname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100,blank=False,unique=True)
    phone = models.CharField(max_length=9,blank=False)
    event =models.CharField(max_length=1000,blank=False)

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name = "Organizator"


class Event(models.Model):
    organizator = models.ForeignKey(Organizator,on_delete=models.CASCADE,related_name='events')
    name = models.CharField(max_length=1000)
    address = models.CharField(max_length=1000)
    location = models.CharField(max_length=1000)
    event_time = models.DateTimeField(editable=True)
    link = models.CharField(max_length=1000,unique=True)

    def __str__(self):
        return self.name

class Participant(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE,related_name='participant')
    fullname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, blank=False)
    phone = models.CharField(max_length=9, blank=False)

    def __str__(self):
        return self.fullname

class Notification(models.Model):
    event = models.ForeignKey(Event, 
                    on_delete=models.CASCADE, 
                    related_name='notification')
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    is_send = models.BooleanField(default=False)
    notify_date = models.DateTimeField()

    def __str__(self):
        event_time_split = str(self.notify_date).split(":")
        event_time = f"{event_time_split[0]}:{event_time_split[1]}"
        return f"{self.event.name} | {event_time} | {self.participant.fullname}"
