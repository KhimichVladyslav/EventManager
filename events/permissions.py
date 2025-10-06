from rest_framework import permissions


class IsOrganizerOrReadOnly(permissions.BasePermission):
    """
    Custom permission class:
    - Read-only access (GET, HEAD, OPTIONS) is allowed for everyone.
    - Write access (edit/delete) is only allowed for the event organizer or admin.
    """

    def has_object_permission(self, request, view, obj):
        # Allow safe methods (read-only requests) for all users
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow full access if the user is an admin (staff)
        if request.user and request.user.is_staff:
            return True

        # Allow editing/deleting only if the user is the organizer of the event
        return obj.organizer == request.user
