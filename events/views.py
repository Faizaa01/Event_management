from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from events.models import Event, Category
from events.forms import Eventform, Categoryform
from django.db.models import Q, Count
from django.contrib import messages
from datetime import date
from django.contrib.auth.models import User



def home(request):
    if request.user.is_authenticated:
        events = Event.objects.select_related('category').prefetch_related('participants').all()
    else:
        events = None
    context = {'data': events, 'query': ''}
    return render(request, 'home.html', context)


# Dashboard

def dashboard(request):
    type = request.GET.get('type','today')
    total_participants = User.objects.filter(rsvp_events__isnull=False).distinct().count()
    total_events = Event.objects.count()
    today = date.today()

    upcoming_events = Event.objects.filter(date__gt=today).count()
    past_events = Event.objects.filter(date__lt=today).count()
    todays_events = Event.objects.filter(date=today)

    if type =='upcoming':
        events_list = Event.objects.filter(date__gt=today).select_related('category').prefetch_related('participants')
    elif type == 'past':
        events_list = Event.objects.filter(date__lt=today).select_related('category').prefetch_related('participants')
    elif type == 'today':
        events_list = todays_events.select_related('category').prefetch_related('participants')
    else:
        events_list = Event.objects.all().select_related('category').prefetch_related('participants')


    context = {
        'total_events': total_events,
        'total_participants': total_participants,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'todays_events': todays_events,
        'events_list': events_list,
        'type': type,
        'today': today
    }
    return render(request, 'dashboard.html', context)


# Search

def search_events(request):
    query = request.GET.get('query', '')
    if query:
        events = Event.objects.filter(Q(name__icontains=query) | Q(location__icontains=query)).select_related('category')
    else:
        events = Event.objects.select_related('category').all()
    return render(request, 'home.html', {'data': events, 'query': query})



# Event

def event_details(request, id):
    event = get_object_or_404(Event.objects.select_related('category').prefetch_related('participants'), id=id)
    participants = event.participants.all()
    context = {
        'event': event,
        'participants': participants,
    }
    return render(request, 'event_details.html', context)


def create_event(request):
    form = Eventform()
    if request.method == "POST":
        form = Eventform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Event Created Successfully.")
            return redirect('create_event')
    context = {"form": form, "title": "Add Event"}
    return render(request, "form.html", context)


def update_event(request, id):
    event = Event.objects.get(id=id)
    if request.method == 'POST':
        form = Eventform(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request,"Event Updated Successfully.")
            return redirect('Event-details', id=event.id)
    else:
        form = Eventform(instance=event)

    context = {"form": form, 'title': 'Update Event'}
    return render(request, "form.html", context)



def delete_event(request, id):
    if request.method == "POST":
        event = Event.objects.get(id=id)
        event.delete()
        messages.success(request, "Event deleted successfully")
        return redirect('home')
    messages.error(request, "Invalid request")
    return redirect('home')


# Participant

# def list_participants(request):
#     data = Participant.objects.prefetch_related('events').all()
#     context = {
#         'data': data,
#         'title': 'Participants List'
#     }
#     return render(request, 'list.html', context)


# def create_participant(request):
#     form = Participantform()
#     if request.method == "POST":
#         form = Participantform(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Participant Created Successfully.")
#             return redirect('create_participant')
#     context = {"form": form, "title": "Add Participant"}
#     return render(request, "form.html", context)


# def update_participant(request, id):
#     participant = Participant.objects.get(id=id)
#     if request.method == 'POST':
#         form = Participantform(request.POST, instance=participant)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Participant Updated Successfully.")
#             if participant.events.exists():
#                 return redirect('Event-details', id=participant.events.first().id)
#             else:
#                 return redirect('list_participants')
#     else:
#         form = Participantform(instance=participant)
#     context = {"form": form, "title": "Update Participant"}
#     return render(request, "form.html", context)


# def delete_participant(request, id):
#     if request.method == "POST":
#         participant = Participant.objects.get(id=id)
#         participant.delete()
#         messages.success(request, "Participant Deleted Successfully.")
#     else:
#         messages.error(request, "Invalid Request")
#     return redirect('list_participants')



# Category

# def list_categories(request):
#     data = Category.objects.all()
#     context = {
#         'data': data,
#         'title': 'Category List'
#     }
#     return render(request, 'list.html', context)


def create_category(request):
    form = Categoryform()
    if request.method == "POST":
        form = Categoryform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category Created Successfully.")
            return redirect('create_category')
    context = {"form": form, "title": "Add Category"}
    return render(request, "form.html", context)


def update_category(request, id):
    category = Category.objects.get(id=id)
    if request.method == 'POST':
        form = Categoryform(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category Updated Successfully.")
            return redirect('list_categories')
    else:
        form = Categoryform(instance=category)
    context = {"form": form, "title": "Update Category"}
    return render(request, "form.html", context)


def delete_category(request, id):
    if request.method == "POST":
        category = Category.objects.get(id=id)
        category.delete()
        messages.success(request, "Category Deleted Successfully.")
    else:
        messages.error(request, "Invalid Request")
    return redirect('list_categories')
