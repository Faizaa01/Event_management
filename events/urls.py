from django.urls import path
from events.views import *

urlpatterns = [
    path('',home, name='home'),
    path('dashboard/',dashboard, name='dashboard'),
    path('search_events/',search_events, name='search'),
    path('events/<int:event_id>/rsvp/', rsvp_event, name='rsvp_event'),
    path('event_details/<int:id>/', EventDetail.as_view(), name='Event-details'),
    # path('event_details/<int:id>/', event_details, name='Event-details'),

    path('list_participants/', list_participants, name='list_participants'),
    path('delete_participant/<int:id>/', delete_participant, name='delete_participant'),


    # path('create_event/',create_event, name='create_event'),
    # path('update_event/<int:id>/', update_event, name='update_event'),
    path('create_event/',CreateEvent.as_view(), name='create_event'),
    path('update_event/<int:id>/', UpdateEvent.as_view(), name='update_event'),
    path('delete_event/<int:id>/', delete_event, name='delete_event'),

    # path('list_categories/', list_categories, name='list_categories'),
    # path('create_category/',create_category, name='create_category'),
    path('list_categories/', ListCategory.as_view(), name='list_categories'),
    path('create_category/',CreateCategory.as_view(), name='create_category'),
    path('update_category/<int:id>/', update_category, name='update_category'),
    path('delete_category/<int:id>/', delete_category, name='delete_category'),
]
