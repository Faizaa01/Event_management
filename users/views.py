from users.forms import RegistrationForm, LoginForm, AssignRoleForm, GroupForm, EditProfileForm, CustomPasswordChangeForm, CustomPasswordResetForm, CustomPasswordResetConfirmForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.contrib.auth import logout
from django.urls import reverse_lazy

User = get_user_model()


def is_admin(user):
    return user.groups.filter(name='Admin').exists()


def no_permission(request):
    return render(request, 'no_permission.html')


def getstarted(request):
    return render(request, 'getstarted.html')


def sign_up(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False
            user.save()
            
            participant_group, created = Group.objects.get_or_create(name='Participant')
            user.groups.add(participant_group)

            return redirect('sign_in')
        else:
            print("Form is not valid")
    return render(request, 'Registration/signup.html', {"form": form})


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'Registration/login.html'

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else super().get_success_url()


# def sign_in(request):
#     form = LoginForm()
#     if request.method == 'POST':
#         form = LoginForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('home')
#     return render(request, 'Registration/login.html', {'form': form})



@login_required
def sign_out(request):
    logout(request)
    return redirect('sign_in')


def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('sign_in')
        else:
            return HttpResponse('Invalid Id or token')

    except User.DoesNotExist:
        return HttpResponse('User not found')
    

# Group

@user_passes_test(is_admin, login_url='no-permission')
def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()

    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
            return redirect('participants_list')

    return render(request, 'admin/assign_role.html', {"form": form})


@user_passes_test(is_admin, login_url='no-permission')
def create_group(request):
    form = GroupForm()
    if request.method == 'POST':
        form = GroupForm(request.POST)

        if form.is_valid():
            group = form.save()
            return redirect('group_list')

    return render(request, 'admin/create_group.html', {'form': form})


@user_passes_test(is_admin, login_url='no-permission')
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, 'admin/group_list.html', {'groups': groups})


# Profile

class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['username'] = user.username
        context['email'] = user.email
        context['name'] = user.get_full_name()
        context['bio'] = user.bio
        context['phone'] = user.phone
        context['profile_image'] = user.profile_image
        context['member_since'] = user.date_joined
        context['last_login'] = user.last_login
        return context
    
class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'form.html'
    context_object_name = 'form'

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save()
        return redirect('profile')
    

# Password

class ChangePassword(PasswordChangeView):
    template_name = 'form.html'
    form_class = CustomPasswordChangeForm


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'form.html'
    success_url = reverse_lazy('sign_in')
    html_email_template_name = 'registration/reset_email.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        return context

    def form_valid(self, form):
        return super().form_valid(form)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name = 'form.html'
    success_url = reverse_lazy('sign_in')

    def form_valid(self, form):
        return super().form_valid(form)
    



