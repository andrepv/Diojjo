from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse

from .forms import UserForm


def signup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            username = user_form.cleaned_data["username"]
            email = user_form.cleaned_data["email"]
            password = user_form.cleaned_data["password1"]
            new_user = User.objects.create_user(username, email, password)
            new_user = authenticate(
                username=username,
                password=password)
            login(request, new_user)
            return redirect('/')
        else:
            return render(request, 'authentication/signup.html', {
                'user_form': user_form})
    else:
        user_form = UserForm()
    return render(request, 'authentication/signup.html', {
        'user_form': UserForm()})


def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)
