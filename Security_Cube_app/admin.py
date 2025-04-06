from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Games)
admin.site.register(Category)
admin.site.register(FrequentlyAskedQuestions)
admin.site.register(FeedbackandRate)
admin.site.register(ContactUs)

from django.apps import AppConfig


class MyAppConfig(AppConfig):
    name = 'Security_Cube_app'

    def ready(self):
        from Security_Cube_app import subscriptions


@admin.register(SubscribedUser)
class SubscribedUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'created']