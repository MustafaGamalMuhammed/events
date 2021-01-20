from django.views.generic import (
    ListView, 
    CreateView, 
    UpdateView, 
    DeleteView, 
    DetailView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from events.models import Event
from events.forms import EventForm
from events.mixins import OwnerRequiredMixin
from accounts.models import CustomUser


class EventListView(ListView):
    model = Event
    template_name = "events/home.html"
    ordering = "date"
    context_object_name = "events"
    paginate_by = 10 

    def get_queryset(self):
        if self._myevents():
            return self.request.user.events.all()
        else:
            return super().get_queryset()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['myevents'] = self._myevents()

        return context

    def _myevents(self):
        return self.request.user.is_authenticated and self.request.GET.get('myevents')


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    template_name = "events/create.html"
    form_class = EventForm

    def get_success_url(self):
        return reverse('events.detail', args=[self.object.id,])


class EventDetailView(DetailView):
    model = Event
    template_name = "events/detail.html"
    context_object_name = "event"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.object.is_owner(self.request)
        context['is_participating'] = self.object.is_participating(self.request)

        return context


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


@login_required
@require_POST
def join_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    event.participants.add(request.user)

    return redirect(event)