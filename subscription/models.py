from django.db import models
from core.models import User
from Security_Cube_app.models import Games 
# Create your models here.



# Subscription plans for Games   
class Plan(models.Model):
    title = models.CharField(max_length=100)
    desc = models.TextField()
    price = models.IntegerField(default=0)
    discount_price = models.IntegerField(default=0)
    discount = models.FloatField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        self.discount_price = self.price - (self.price* self.discount)
        super().save(*args, **kwargs)
    

    class Meta:
        ordering = ("created_on",)
    
    def __str__(self):
        return self.title
    

    
# User Subscription     
class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_subscription')
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    expiring_date = models.DateField(null=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan.title}"


    