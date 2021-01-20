from django.views.generic import (
    ListView, 
    CreateView, 
    UpdateView, 
    DeleteView, 
    DetailView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from events.models import Event
from events.forms import EventForm
from events.mixins import OwnerRequiredMixin


class EventListView(ListView):
    model = Event
    template_name = "events/home.html"
    ordering = "date"
    context_object_name = "events"


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    template_name = "events/create.html"
    form_class = EventForm

    def get_success_url(self):
        return reverse('events.detail', args=[self.object.id,])


class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = "events/detail.html"
    context_object_name = "event"


class EventUpdateView(OwnerRequiredMixin, UpdateView):
    model = Event
    template_name = "events/update.html"
    form_class = EventForm
    context_object_name = "event"

    def get_success_url(self):
        return reverse('events.detail', args=[self.object.id,])


class EventDeleteView(OwnerRequiredMixin, DeleteView):
    model = Event
    template_name = "events/delete.html"
    context_object_name = "event"

    def get_success_url(self):
        return reverse('events')