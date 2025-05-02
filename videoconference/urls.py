from django.urls import path
from .views import get_livekit_token
from .views import videochat

app_name = 'videoconference'

urlpatterns = [
    path('get-livekit-token/', get_livekit_token, name='get_livekit_token'),
    path('videochat/', videochat, name='videochat'),

]
