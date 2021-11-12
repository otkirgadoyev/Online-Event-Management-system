from django.contrib import admin

from .models import Organizator,Event,Notification,Participant
class OrganizatorAdmin(admin.ModelAdmin):
    list_display=(
        'fullname', 'email','phone'
    )
class EventAdmin(admin.ModelAdmin):
    list_display=(
        'name','organizator','address','location','event_time','link'
    )
class ParticipantAdmin(admin.ModelAdmin):
    list_display=(
        'fullname', 'email','phone'
    )
class NotificationAdmin(admin.ModelAdmin):
    list_display=[
        'event', 'participant','notify_date','is_send'
    ]

admin.site.register(Organizator,OrganizatorAdmin)
admin.site.register(Event,EventAdmin)
admin.site.register(Participant,ParticipantAdmin)
admin.site.register(Notification, NotificationAdmin)
