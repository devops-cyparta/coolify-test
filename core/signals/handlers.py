from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone 
from ..models import Customer, User, Level 
from subscription.models import Subscription, Plan 

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_for_new_user(sender, **kwargs):
  if kwargs['created']:
    Customer.objects.create(user=kwargs['instance'])



# Set default value for level 
@receiver(post_save, sender=User)
def set_default_level(sender, instance, created, **kwargs):
    """
    Signal to set default levels for a new user and update levels based on points.
    """
    if created:  # Only for newly created users
        levels = Level.objects.all().order_by('points')

        if levels.exists():
            default_level = levels.first()
            instance.current_level = default_level

            # Find the first level with points greater than the default level's points
            next_level = levels.filter(points__gt=default_level.points).first()

            # If there is no next level, set it to the highest level
            instance.next_level = next_level or levels.last()

            instance.save()

    # Disconnect the signal to avoid recursion
    post_save.disconnect(set_default_level, sender=User)

    # Update levels based on points
    levels = Level.objects.all().order_by('points')

    current_level = None
    next_level = None

    for level in levels:
        if instance.points < level.points:
            next_level = level
            break
        current_level = level

    # If the loop completes without breaking, get the least level
    current_level = current_level or levels.first()

    instance.current_level = current_level
    instance.next_level = next_level
    instance.save()

    # Reconnect the signal
    post_save.connect(set_default_level, sender=User)


# Create Default Subscription
def create_default_subscription(sender, instance, created, **kwargs):
    if created:
        try:
            default_plan = Plan.objects.get(title='Basic')  
        except Plan.DoesNotExist:
            return None 
        
        
        Subscription.objects.create(user=instance, plan=default_plan)
