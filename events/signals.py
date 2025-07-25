from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from events.models import Event

@receiver(m2m_changed, sender=Event.participants.through)
def notify_user_on_rsvp(sender, instance, action, **kwargs):
    if action == 'post_add':
        participant_emails = [user.email for user in instance.participants.all()]
        # print("RSVP email check....", participant_emails)
        send_mail(
            "RSVP Confirmation",
            f"You have successfully RSVPed to the event: {instance.name}",
            "faizaniha0062@gmail.com",
            participant_emails,
            fail_silently=False,
        )

