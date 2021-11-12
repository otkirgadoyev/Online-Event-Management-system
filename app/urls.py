from django.urls import path
from . import views
urlpatterns = [
    path('register-organizator/',views.RegisterView.as_view(),name='register-organizator'),
    path('event-add/',views.AddEventView.as_view(),name='event-add-organizator'),
    path('register-participant/',views.RegisterParticipantView.as_view(),name='register-participant'),
    path('event/<str:link_id>/',views.AddEventDetail.as_view(),name='event'),
]