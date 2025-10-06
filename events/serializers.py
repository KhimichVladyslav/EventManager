from rest_framework import serializers

from .models import Event, EventRegistration


class EventSerializer(serializers.ModelSerializer):
    """
    Serializer for Event model.
    - Exposes all event fields.
    - Organizer is read-only and represented by the username.
    """

    organizer = serializers.ReadOnlyField(source="organizer.username")

    class Meta:
        model = Event
        fields = "__all__"


class EventRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for EventRegistration model.
    - The `user` field is read-only and automatically set from the request.
    - Prevents duplicate registrations for the same event by the same user.
    """

    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = EventRegistration
        fields = ["id", "user", "event", "registered_at"]
        read_only_fields = ["id", "user", "registered_at"]

    def validate(self, attrs):
        """
        Custom validation:
        - Ensures that the request is authenticated.
        - Prevents a user from registering for the same event more than once.
        """
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Authentication required.")

        event = attrs.get("event")
        if EventRegistration.objects.filter(user=request.user, event=event).exists():
            raise serializers.ValidationError("Already registered for this event.")

        return attrs

    def create(self, validated_data):
        """
        Automatically assign the current user as the registration owner.
        """
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
