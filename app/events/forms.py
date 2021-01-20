from django import forms
from events.models import Event
from django.utils import timezone 
from django.utils.translation import gettext as _


def present_or_future_date(value):
    if value < timezone.now():
        raise forms.ValidationError(_("The date cannot be in the past!"), code="invalid")
    return value


class EventForm(forms.ModelForm):
    date = forms.DateTimeField(validators=[present_or_future_date])

    class Meta:
        model = Event
        fields = ['owner', 'title', 'description', 'date']