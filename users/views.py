from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.tokens import default_token_generator
from users.forms import RegistrationForm, LoginForm, AssignRoleForm, GroupForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.decorators import login_required, user_passes_test




def is_admin(user):
    return user.groups.filter(name='Admin').exists()



def no_permission(request):
    return render(request, 'no_permission.html')


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




def sign_in(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    return render(request, 'Registration/login.html', {'form': form})



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

