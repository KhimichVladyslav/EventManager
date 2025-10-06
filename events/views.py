from rest_framework import filters, permissions, viewsets

from .models import Event, EventRegistration
from .permissions import IsOrganizerOrReadOnly
from .serializers import EventRegistrationSerializer, EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    """
    CRUD for events.
    - Read: all users
    - Create: authenticated
    - Update/Delete: organizer or admin
    - Supports search & filtering
    """

    queryset = Event.objects.select_related("organizer").all().order_by("date")
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOrganizerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "location", "description"]
    filterset_fields = {
        "date": ["gte", "lte"],
        "organizer__username": ["exact"],
    }

    def perform_create(self, serializer):
        """Set organizer to the current user."""
        serializer.save(organizer=self.request.user)


class EventRegistrationViewSet(viewsets.ModelViewSet):
    """
    Manage event registrations.
    - Only authenticated users
    - Prevent duplicate registrations
    """

    queryset = EventRegistration.objects.select_related("user", "event").order_by("-registered_at")
    serializer_class = EventRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]
    swagger_tags = ["Registrations"]

    def perform_create(self, serializer):
        """Assign current user to the registration."""
        serializer.save(user=self.request.user)
