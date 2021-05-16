from django.shortcuts import render
from . import api


def dashboard(request):
    return render(request, 'dashboard.html')


def votes(request):
    return render(request, 'votes.html')
