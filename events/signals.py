from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.dateparse import parse_datetime

from .models import EventRegistration


@receiver(post_save, sender=EventRegistration)
def send_registration_email(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        first_name = user.username

        event_date = instance.event.date
        if isinstance(event_date, str):
            event_date = parse_datetime(event_date)

        subject = f"Registration Confirmed for {instance.event.title}"
        message = (
            f"Hello {first_name},\n\n"
            f'You have successfully registered for the event "{instance.event.title}" 🎉.\n\n'
            f"📅 Date: {event_date.strftime('%Y-%m-%d %H:%M')}\n"
            f"📍 Location: {instance.event.location}\n\n"
            f"We look forward to seeing you!\n\n"
            f"Best regards,\n"
            f"Event Manager Team"
        )

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
