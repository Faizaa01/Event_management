from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from users.forms import RegistrationForm, LoginForm



def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, 'Account created successfully. Please login.')
            return redirect('sign_in')
    else:
        form = RegistrationForm()
    return render(request, 'registration/signup.html', {'form': form})




def sign_in(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    return render(request, 'registration/login.html', {'form': form})




def sign_out(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('sign_in')