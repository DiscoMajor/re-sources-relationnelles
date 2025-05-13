from django.utils import timezone
from django.shortcuts import render, HttpResponseRedirect
from visio.models import Meeting
from .forms import MeetingCreateForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages

# Create your views here.
def home(request):
    form = MeetingCreateForm()
    if request.method == 'POST':
        form = MeetingCreateForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.creator = request.user
            meeting.save()
            messages.success(request, "Réunion créée avec succès !")
            return HttpResponseRedirect(reverse('visio:meeting_list'))
    return render(request, 'visio/home.html', {'form': form})

@login_required()
def meeting_list(request):
    user = request.user
    meetings = Meeting.objects.filter(creator=user) 

    return render(request, 'visio/meeting_list.html', {'meetings': meetings})

def meeting(request, unique_meeting_name):
    meeting = Meeting.objects.filter(unique_meeting_name=unique_meeting_name).first()
    context = {
        'meeting': meeting,
        'current_time': timezone.now()
    }
    if not request.user == meeting.creator:
        """check to know if the current user is not the creator of the meeting
        if True, then the guest page template will be rendered."""
        return render(request, 'visio/guest.html', context)

    return render(request, 'visio/video_call.html', context)