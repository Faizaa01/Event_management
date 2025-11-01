from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView
from django.shortcuts import render, redirect,get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.base import ContextMixin
from events.forms import Eventform, Categoryform
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from events.models import Event, Category
from django.db.models import Prefetch
from django.db.models import Q, Count
from django.contrib import messages
from users.views import is_admin
from django.views import View
from datetime import date

User = get_user_model()



def is_participant(user):
    return user.groups.filter(name="Participant").exists()


def home(request):
    if request.user.is_authenticated:
        events = Event.objects.select_related('category').prefetch_related('participants').all()
    else:
        events = None
    context = {'data': events, 'query': ''}
    return render(request, 'home.html', context)



# RSVP

@user_passes_test(is_participant)
def rsvp_event(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.user not in event.participants.all():
        event.participants.add(request.user)
    return redirect('Event-details', id=event_id)




# Dashboard
@login_required
def dashboard(request):
    today = date.today()
    type = request.GET.get('type','today')
    rsvp_events = request.user.rsvp_events.all().count()
    total_participants = User.objects.filter(rsvp_events__isnull=False).distinct().count()
    total_events = Event.objects.count()

    role = 'Participant'
    if request.user.groups.filter(name='Admin').exists():
        role = 'Admin'
    elif request.user.groups.filter(name='Organizer').exists():
        role = 'Organizer'

    if role == 'Participant':
        upcoming_events = request.user.rsvp_events.filter(date__gt=today).count()
        past_events = request.user.rsvp_events.filter(date__lt=today).count()
        todays_events = request.user.rsvp_events.filter(date=today)
    else:
        upcoming_events = Event.objects.filter(date__gt=today).count()
        past_events = Event.objects.filter(date__lt=today).count()
        todays_events = Event.objects.filter(date=today)


    if role == 'Participant' and request.user.is_authenticated:
        user_events = request.user.rsvp_events.all()
        if type == 'upcoming':
            events_list = user_events.filter(date__gt=today).select_related('category')
        elif type == 'past':
            events_list = user_events.filter(date__lt=today).select_related('category')
        elif type == 'today':
            events_list = user_events.filter(date=today).select_related('category')
        elif type == 'all':
            events_list = Event.objects.all().select_related('category').prefetch_related('participants')
        else:
            events_list = user_events.select_related('category')
    else:
        if type == 'upcoming':
            events_list = Event.objects.filter(date__gt=today).select_related('category').prefetch_related('participants')
        elif type == 'past':
            events_list = Event.objects.filter(date__lt=today).select_related('category').prefetch_related('participants')
        elif type == 'today':
            events_list = todays_events
        else:
            events_list = Event.objects.all().select_related('category').prefetch_related('participants')

    context = {
        'total_events': total_events,
        'total_participants': total_participants,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'todays_events': todays_events,
        'events_list': events_list,
        'rsvp_events': rsvp_events,
        'type': type,
        'today': today,
        'role': role
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

class EventDetail(DetailView):
    model = Event
    pk_url_kwarg = 'id'
    context_object_name = 'event'
    template_name = 'event_details.html'

    def get_queryset(self):
        return Event.objects.select_related('category').prefetch_related('participants')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["participants"] = self.object.participants.all()
        return context
    


class CreateEvent(ContextMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'events.add_event'
    template_name = 'form.html'
    login_url = 'sign_in'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = kwargs.get('form', Eventform())
        context['title'] = 'Add Event'
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = Eventform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('create_event')
        context = self.get_context_data(form = form)
        return render(request, self.template_name, context)


class UpdateEvent(PermissionRequiredMixin, UpdateView):
    model = Event
    pk_url_kwarg = 'id'
    form_class = Eventform
    template_name = 'form.html'
    login_url = 'no-permission'
    context_object_name = 'event'
    permission_required = 'events.change_event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Update Event'
        return context
    
    def form_valid(self, form):
        event = form.save()
        return redirect('Event-details', id=event.id)
    


@permission_required("events.delete_event", login_url='no-permission')
def delete_event(request, id):
    if request.method == "POST":
        event = Event.objects.get(id=id)
        event.delete()
        return redirect('home')
    messages.error(request, "Invalid request")
    return redirect('home')


@user_passes_test(is_admin, login_url='no-permission')
def participants_list(request):
    users = User.objects.prefetch_related(Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')).all()
    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = 'No Group Assigned'

    return render(request, 'admin/participants_list.html', {'users': users})


# participants

@user_passes_test(is_admin, login_url='no-permission')
def list_participants(request):
    participants = User.objects.filter(groups__name='Participant').prefetch_related('rsvp_events').distinct()
    context = {
        'data': participants,
        'title': 'Participants List'
    }
    return render(request, 'list.html', context)



@permission_required("events.delete_participant", login_url='no-permission')
def delete_participant(request, id):
    if request.method == "POST":
        participant = get_object_or_404(User, id=id, groups__name='Participant')
        participant.delete()
        messages.success(request, "Participant deleted successfully.")
    else:
        messages.error(request, "Invalid request.")
    return redirect('list_participants')




# Category

view_category_decorators = [login_required, permission_required("events.view_category", login_url='no-permission')]
@method_decorator(view_category_decorators, name='dispatch')
class ListCategory(ListView):
    model = Category
    template_name = 'list.html'
    context_object_name = 'data'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Category List'
        return context
    def get_queryset(self):
        queryset = Category.objects.annotate(num=Count('events')).order_by('num')
        return queryset



class CreateCategory(ContextMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'events.add_category'
    login_url = 'sign_in'
    template_name = 'form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = kwargs.get('form', Categoryform())
        context['title'] = 'Add Category'
        return context


    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = Categoryform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_categories')
        context = self.get_context_data(form = form)
        return render(request, self.template_name, context)


@permission_required("events.change_category", login_url='no-permission')
def update_category(request, id):
    category = Category.objects.get(id=id)
    if request.method == 'POST':
        form = Categoryform(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('list_categories')
    else:
        form = Categoryform(instance=category)
    context = {"form": form, "title": "Update Category"}
    return render(request, "form.html", context)


@permission_required("events.delete_category", login_url='no-permission')
def delete_category(request, id):
    if request.method == "POST":
        category = Category.objects.get(id=id)
        category.delete()
    else:
        messages.error(request, "Invalid Request")
    return redirect('list_categories')
