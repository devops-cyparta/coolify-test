from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import User

class Command(BaseCommand):
    help = 'Reset daily targets for all users.'

    def handle(self, *args, **options):
        # Get all users and reset their daily targets to zero
        users = User.objects.all()
        for user in users:
            user.achieved_daily_target = False 
            user.save()


        self.stdout.write(self.style.SUCCESS('Successfully reset daily targets for all users.'))
