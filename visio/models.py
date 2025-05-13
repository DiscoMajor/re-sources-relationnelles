from django.db import models
from django.utils import timezone
import uuid
from django.utils.text import slugify
from datetime import timedelta


class Meeting(models.Model):
    creator = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='created_meeting')
    title_of_meeting = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    duration = models.PositiveIntegerField(default=60)
    starting_date_time = models.DateTimeField()
    ending_date_time = models.DateTimeField()
    unique_meeting_name = models.TextField(blank=True, null=True)

    @property
    def meeting_status(self):
        now = timezone.now()
        if now < self.starting_date_time:
            return "not_started"
        elif now > self.ending_date_time:
            return "ended"
        else:
            return "ongoing"

    def __str__(self):
        return f"{self.creator}: {self.title_of_meeting}"

    def save(self, *args, **kwargs):
        if self.duration:
            self.ending_date_time = self.starting_date_time + timedelta(minutes=self.duration)

        if not self.unique_meeting_name:
            self.unique_meeting_name = slugify(
                f"{self.title_of_meeting}-{uuid.uuid4()}"
            )
        
        super().save(*args, **kwargs)