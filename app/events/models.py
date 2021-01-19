from django.db import models
from accounts.models import CustomUser


class Event(models.Model):
    owner = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name="owned_events")

    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    participants = models.ManyToManyField(
        CustomUser, 
        blank=True, 
        related_name="events")
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.title