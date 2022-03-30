from django.http import HttpResponse, Http404
from django.shortcuts import render, get_list_or_404

from .models import Monster, Evolution


def index(request):
    try:
        monsters = Monster.objects.all()
    except Monster.DoesNotExist:
        raise Http404
    return render(request, 'monsters/index.html', {'monsters': monsters})


def detail(request, monster_id):
    try:
        monster = Monster.objects.get(pk=monster_id)
    except Monster.DoesNotExist:
        raise Http404

    pre_evolution = None
    pre_evolutions = Evolution.objects.filter(next_evolution=monster)
    if pre_evolutions:
        pre_evolution = pre_evolutions[0]
    evolutions = Evolution.objects.filter(pre_evolution=monster)
    return render(request, 'monsters/detail.html', {
        'monster': monster,
        'pre_evolution': pre_evolution,
        'evolutions': evolutions
    })
