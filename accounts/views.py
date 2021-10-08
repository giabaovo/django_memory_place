from django.shortcuts import render
from django.dispatch import receiver
from allauth.socialaccount.signals import social_account_added


def index(request):
    return render(request, 'accounts/profiles.html')
