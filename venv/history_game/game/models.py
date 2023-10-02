from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Event(models.Model):
    # Fields
    name = models.CharField(max_length=50, help_text='Enter event name (20 characters)')
    date = models.DateField()
    description = models.TextField(max_length=500, help_text='Enter event description (200 characters)')
    topic = models.CharField(max_length=50, null=True, blank=True)
    category = models.CharField(max_length=50, null=True, blank=True)

    # Metadata
    class Meta:
        ordering = ['date', 'name']

    # Methods
    def get_absolute_url(self):
        """Returns the URL to access a particular instance of Event."""
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.name


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    highscore = models.IntegerField(default=0)

    # Metadata
    class Meta:
        ordering = ['id']

    # Methods
    def get_absolute_url(self):
        """Returns the URL to access a particular instance of Event."""
        return reverse('model-detail-view', args=[str(self.username)])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.username


class Match(models.Model):
    # Fields
    event_list = models.ManyToManyField(Event)
    game_won = models.BooleanField(default=False)
    user_playing = models.ForeignKey(User,on_delete=models.CASCADE)

    # Metadata
    class Meta:
        ordering = ['id']

    # Methods
    def get_absolute_url(self):
        """Returns the URL to access a particular instance of Match."""
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.id)
