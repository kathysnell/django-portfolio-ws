from .models import Intro

def global_intro(request):
    intro_data = Intro.objects.filter(active=True).first()
    return {'intro': intro_data}
