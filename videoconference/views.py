from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from livekit import api
import os
# Create your views here.
@csrf_exempt
def get_livekit_token(request):
    room_name = request.GET.get('room', 'default-room')
    identity = str(request.user.id)
    token = api.AccessToken(os.getenv('LIVEKIT_API_KEY'), os.getenv('LIVEKIT_API_SECRET')) \
    .with_identity(identity) \
    .with_name(request.user.username) \
    .with_grants(api.VideoGrants(
        room_join=True,
        room=room_name)) \
    .with_sip_grants(api.SIPGrants(
      admin=True,
      call=True)).to_jwt()
    return JsonResponse({
      "token": token,})

def videochat(request):
  return render(request, 'videochat.html')