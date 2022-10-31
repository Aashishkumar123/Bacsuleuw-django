from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import User
from .models import Profile


@receiver(post_save, sender = User)
def send_activation_email(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
