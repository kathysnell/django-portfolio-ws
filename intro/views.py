from django.shortcuts import render
from .models import Intro
from django.views.decorators.http import require_GET

@require_GET
def intro(request):
    intro_data = Intro.objects.first()
    context = {
        'intro_data': intro_data,
    }
    return render(request, 'intro/intro.html', context)

