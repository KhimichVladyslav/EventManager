from django.contrib.auth.models import User
from django.db import models


class Event(models.Model):
    """
    Represents an event created by a user (organizer).
    Includes basic details like title, description, date, and location.
    """

    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    date = models.DateTimeField(db_index=True)
    location = models.CharField(max_length=255, db_index=True)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="organized_events")

    def __str__(self):
        return self.title


class EventRegistration(models.Model):
    """
    Represents a user's registration for a specific event.
    Ensures a user can register for the same event only once.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="event_registrations")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="registrations")
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "event")
