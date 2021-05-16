from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from . import api


def dashboard(request):
    return render(request, 'dashboard.html')


@login_required
def votes(request):
    return render(request, 'votes.html')
