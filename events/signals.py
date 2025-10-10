from django.db.models.signals import m2m_changed
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.dispatch import receiver
from events.models import Event

User = get_user_model()

@receiver(m2m_changed, sender=Event.participants.through)
def rsvp_activation_mail(sender, instance, action, pk_set=None, **kwargs):
    if action == 'post_add':
        participant_emails = [user.email for user in User.objects.filter(pk__in=pk_set)]
        # print("RSVP email check....", participant_emails)
        send_mail(
            "RSVP Confirmation",
            f"Congratulations!!! You have successfully Reserved to the event: {instance.name}",
            "faizaniha0062@gmail.com",
            participant_emails,
            fail_silently=False,
        )

