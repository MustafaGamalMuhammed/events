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
from django.contrib import messages

from events.models import Event
from events.forms import EventForm
from events.mixins import OwnerRequiredMixin
from accounts.models import CustomUser


class EventListView(ListView):
    model = Event
    template_name = "events/home.html"
    ordering = "date"
    context_object_name = "events"
    paginate_by = 5

    def get_queryset(self):
        """
        If the user is authenticated and there is a myevents query parameter; 
        return the user's events otherwise return all events
        """
        if self._myevents():
            owned_events = self.request.user.owned_events.all()
            participating_events = self.request.user.events.all()

            queryset = (owned_events | participating_events) 
        else:
            queryset = super().get_queryset()

        for q in queryset:
            q.is_participanting = q._is_participating(self.request)
            q.is_owner = q._is_owner(self.request)

        return queryset
    
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

    def form_invalid(self, form):
        for error in form.errors:
            messages.error(self.request, form.errors[error])

        return super().form_invalid(form)


class EventDetailView(DetailView):
    model = Event
    template_name = "events/detail.html"
    context_object_name = "event"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.object._is_owner(self.request)
        context['is_participating'] = self.object._is_participating(self.request)

        return context


class EventUpdateView(OwnerRequiredMixin, UpdateView):
    model = Event
    template_name = "events/update.html"
    form_class = EventForm
    context_object_name = "event"

    def get_success_url(self):
        return reverse('events.detail', args=[self.object.id,])

    def form_invalid(self, form):
        for error in form.errors:
            messages.error(self.request, form.errors[error])

        return super().form_invalid(form)


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


@login_required
@require_POST
def withdraw_from_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    out = event.participants.remove(request.user)

    return redirect(event)