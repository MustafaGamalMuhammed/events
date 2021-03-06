from django.db import models
from django.urls import reverse
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

    def get_absolute_url(self):
        return reverse('events.detail', args=[self.id,])

    def _is_owner(self, request):
        """Is the user the owner of the event?"""
        return request.user.is_authenticated and request.user == self.owner

    def _is_participating(self, request):
        """Is the user participating in the event?"""
        return request.user.is_authenticated and self.participants.filter(pk=request.user.pk).exists()
