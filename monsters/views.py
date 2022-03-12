from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404

from .models import Monster


def index(request):
    return HttpResponse("Hello, These are monsters")


def detail(request, monster_id):
    try:
        monster = Monster.objects.get(pk=monster_id)
    except Monster.DoesNotExist:
        raise Http404
    return render(request, 'monsters/detail.html', {'monster': monster})
