from django.core.management.base import BaseCommand
from app.models import * 
from datetime import datetime, timedelta
from app.serializers import *
from app.utils import Util
from app.models import Notification

class Command(BaseCommand):
    def handle(self, *args, **options):
        today = datetime.today()
        print(today)
        notifications = Notification.objects.filter(
            is_send=False,
            notify_date__year__lte = today.year,
            notify_date__month__lte = today.month,
            notify_date__day__lte = today.day,
            notify_date__hour__lte = today.hour,
            )
        counter = 0
        for notification in notifications:
            to_event = notification.event.event_time-today
            if to_event.days!=0:
                to_event = f"{to_event.days} kun"
            else:
                to_event = f"{to_event.hours} soat"
                
            email_body = "<html>"\
                         f"Assalomu alaykum {notification.participant.fullname}! "\
                         f"Sizni {notification.event.event_time} da bo'ladigan "\
                         f"{notification.event.name} tadbiriga {to_event} qolganligi "\
                         f"haqida xabar beramiz. Tadbirga o'z vaqtida kelishni unutmang."\
                         "\n\n Hurmat bilan event.uz </html>"
            data = {
                'email_body': email_body,
                'to_email': notification.participant.email,
                'email_subject': f'{notification.event.name} {to_event} qoldi!'
            }
            Util.send_email(data)
            notification.is_send=True
            notification.save()
            counter += 1
        print(f"Jo'natilgan xabarlar soni: {counter}")