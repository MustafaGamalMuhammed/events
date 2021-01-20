from django.urls import path
from events import views


urlpatterns = [
    path('events/', views.EventListView.as_view(), name='events'),
    path('events/create/', views.EventCreateView.as_view(), name='events.create'),
    path('events/<int:pk>/', views.EventDetailView.as_view(), name='events.detail'),
    path('events/<int:pk>/update', views.EventUpdateView.as_view(), name='events.update'),
    path('events/<int:pk>/delete', views.EventDeleteView.as_view(), name='events.delete'),
    path('events/<int:pk>/join/', views.join_event, name="events.join"),
    path('', views.EventListView.as_view(), name='home'),
]