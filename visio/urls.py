from django.urls import path
from . import views

app_name = "visio"

urlpatterns = [
    path("", views.home, name="video_call"),
    path('mes-reunions/', views.meeting_list, name='meeting_list'),
    path('live-meeting/<str:unique_meeting_name>/', views.meeting, name='meeting'),
]