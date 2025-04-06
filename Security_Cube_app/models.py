from django.db import models
from multiselectfield import MultiSelectField
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from core.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Category(models.Model):
    title=models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.title

# Game Model 
class Games(models.Model):
    MY_CHOICES = (('Multiplayer', 'Multiplayer'),
        ('Single player', 'Single player')
        )

    pic = models.ImageField(upload_to='Games',default='1048227_1_AMADpCo.png')
    game_file = models.URLField()
    name = models.CharField(max_length=100)
    description  = models.TextField(max_length=500)
    features  = MultiSelectField(choices=MY_CHOICES,max_choices=2 ,max_length=50 )
    how_to_play = models.TextField(max_length=500)
    game_points = models.IntegerField()
    released_date = models.DateField(null=True) 
    category = models.ManyToManyField(Category,related_name='game_category')
    premium_plan = models.ManyToManyField('subscription.Plan')

    # ... (existing methods)

    @property
    def is_premium(self):
        return self.premium_plan is not None
    def __str__(self) -> str:
        return self.name
    
    @property
    def feedbacks(self):
        return self.game_feedback.all()


# Frequently Asked Question Model 
class FrequentlyAskedQuestions(models.Model):
    Frequently_asked_questions = models.TextField()
    answer = models.TextField()
    def __str__(self):
        return self.Frequently_asked_questions 

    class Meta:
        ordering = ['-id']


class FeedbackandRate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_rate')
    games = models.ForeignKey(Games, on_delete=models.CASCADE,related_name='game_feedback')
    title = models.CharField(max_length=200)
    test = models.CharField(max_length=200, blank=True, null=True)
    feedback = models.CharField(max_length=500)
    stars = models.PositiveBigIntegerField(validators=[MaxValueValidator(5),MinValueValidator(1)])
    date = models.DateTimeField(default=timezone.now)




# Contact Reasons 
class ContactReason(models.Model):
    title = models.CharField(max_length=500)
    def __str__(self):
        return self.title 
    


# Contact Us 
class ContactUs(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = PhoneNumberField(max_length=20)
    contact_reason = models.ForeignKey(ContactReason, on_delete=models.CASCADE),
    # user = models.ForeignKey(User, related_name='contact_us_user', on_delete=models.CASCADE, null=True)
    message = models.TextField()

    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name_plural = 'Contact Us'
        ordering = ['-id']


class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_goal')
    set_time = models.TimeField()
    start_time = models.TimeField(default=timezone.now)
    end_time = models.TimeField(blank=True, null=True)

    def __str__(self):
        return self.user.first_name  





# Subscribed Users 
class SubscribedUser(models.Model):
    email = models.EmailField(unique=True, max_length=60)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    def __str__(self):
        return self.email 
