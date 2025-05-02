from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import create_livekit_token
import json

# Create your views here.
@csrf_exempt
def get_livekit_token(request):
  if request.method == 'POST':
    data = json.loads(request.body)
    identity = data.get('identity')

    if not identity:
      return JsonResponse({'error': 'Identity is required'}, status=400)

    token = create_livekit_token(identity)
    return JsonResponse({'token': token})
  
  return JsonResponse({'error': 'Invalid request method'}, status=405)


def videochat(request):
  return render(request, 'videochat.html')