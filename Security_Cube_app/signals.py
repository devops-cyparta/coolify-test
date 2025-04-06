from .models import *
from django.dispatch import receiver
from django.db.models.signals import post_save
# create my signals

# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created=False, **kwargs):
#     if created:
#         if not instance.is_superuser:
#             pass
#             instance.set_password(instance.password)
#             instance.save()
#         instance.username=instance.email.split('@')[0]
#         instance.save()
    