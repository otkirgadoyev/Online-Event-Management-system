import uuid
from datetime import datetime, timedelta

from dj_rest_auth.app_settings import JWTSerializer
from dj_rest_auth.utils import jwt_encode
from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *
from .utils import Util


class RegisterView(APIView):
    permission_classes=[AllowAny]

    def get(self, request):
        organizator = Organizator.objects.all()
        serializer = RegisterOrganizatorSerializer(organizator, many=True)
        return Response(serializer.data)
    @swagger_auto_schema(request_body=RegisterOrganizatorSerializer)
    def post(self, request):
        request.data['username'] = str(uuid.uuid4().hex)
        serializer = RegisterOrganizatorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user_id = serializer.data['id']
            user_obj = Organizator.objects.get(id=user_id)
            access_token, refresh_token = jwt_encode(user_obj)
            data = {
                'user': user_obj,
                'access_token': access_token,
                'refresh_token': refresh_token,
            }
            return Response(JWTSerializer(data, context=serializer).data,
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AddEventView(APIView):
    permission_classes =[IsAuthenticated]
    
    def get(self, request):
        event=Event.objects.all()
        serializer=EventSerializer(event, many=True)
        return Response(serializer.data)
        
    @swagger_auto_schema(request_body=EventSerializer)
    def post(self, request, format=None):
        events = Event.objects.all()
        for event in events:
            pk=event.id+1
        request.data['organizator'] = request.user.id
        request.data['link']= 'http://127.0.0.1:8000/api/v1/event/'+str(uuid.uuid4().hex)[10]+'/'
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


class AddEventDetail(APIView):
    permission_classes =[IsAuthenticated]
    def get_object(self, link_id):
        try:
            return Event.objects.get(link='http://127.0.0.1:8000/api/v1/event/'+link_id+'/')
        except Event.DoesNotExist:
            raise Http404

    def get(self, request, link_id, format=None):
        event = self.get_object(link_id)
        serializer = EventSerializer(event)
        return Response(serializer.data)

class RegisterParticipantView(APIView):
    permission_classes=[AllowAny]

    def get(self, request):
        participant=Participant.objects.all()
        serializer=RegisterParticipantSerializer(participant, many=True)
        return Response(serializer.data)
    
    def set_notifications(self, event, user):
        a_day_to_event = event.event_time-timedelta(days=1)
        four_hour_to_event = event.event_time-timedelta(hours=4)
        for event_date in [a_day_to_event, four_hour_to_event]:
            notification = Notification(
                            event=event, 
                            participant=user,
                            notify_date = event_date
                        )
            notification.save()

    def send_register_mail(self, request_data, event_object):
            event_link=event_object.link
            email_body="<html>"\
                        f"Assalomu alaykum {request_data['fullname']}! "\
                        f"Sizni {event_object.event_time.date} kuni bo'ladigan tadbirga "\
                        "muvaffaqiyatli ro'yxatdan o'tqazilganingiz haqida xabardor "\
                        "qilishdan mamnunmiz. \n\n"\
                        "Tadbir haqida ma'lumot olish uchun quyidagi havoladan "\
                        f"foydalanishingiz mumkin: <a href=\"{event_link}\">havola</a>"\
                        "\n\n Hurmat bilan event.uz ma'muriyati!"\
                        "</html>"
            data = {
                    'email_body':email_body,
                    'to_email':request_data['email'],
                    'email_subject':f'{event_object.name}'
                }

            Util.send_email(data)

    @swagger_auto_schema(request_body=RegisterParticipantSerializer)
    def post(self, request):
        """Event uchun tadbir qatnashchilarini ro'yhatdan o'tkazish """

        request_data = request.data
        event_object = Event.objects.get(id=request_data['event'])
        serializer = RegisterParticipantSerializer(data=request_data)
        
        if serializer.is_valid():
            serializer.save()
            self.send_register_mail(request_data, event_object)
            self.set_notifications(event_object, serializer.data['user'])

            return Response({"detail": "Participant has been successfully registered"},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




