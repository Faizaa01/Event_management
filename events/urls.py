from django.urls import path
from events.views import *

urlpatterns = [
    path('',home, name='home'),
    path('dashboard/',dashboard, name='dashboard'),
    path('search_events/',search_events, name='search'),
    # path('list/<str:item_type>/', list_items, name='list_items'),
    # path('participants/', list_participants, name='list_participants'),
    # path('categories/', list_categories, name='list_categories'),


    path('event_details/<int:id>/', event_details, name='Event-details'),
    path('create_event/',create_event, name='create_event'),
    path('update_event/<int:id>/', update_event, name='update_event'),
    path('delete_event/<int:id>/', delete_event, name='delete_event'),

    # path('create_participant/',create_participant, name='create_participant'),
    # path('update_participant/<int:id>/',update_participant, name='update_participant'),
    # path('delete_participant/<int:id>/',delete_participant, name='delete_participant'),

    path('create_category/',create_category, name='create_category'),
    path('update_category/<int:id>/', update_category, name='update_category'),
    path('delete_category/<int:id>/', delete_category, name='delete_category'),
]
