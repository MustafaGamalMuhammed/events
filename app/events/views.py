from django.views.generic import (
    ListView, 
    CreateView, 
    UpdateView, 
    DeleteView, 
    DetailView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from events.models import Event
from events.forms import EventForm


class EventListView(ListView):
    model = Event
    template_name = "events/home.html"
    ordering = "date"


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    template_name = "events/create.html"
    form_class = EventForm


class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = "events/detail.html"


class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    template_name = "events/update.html"
    form_class = EventForm


class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = Event
    template_name = "events/delete.html"