from urllib import request

from django.shortcuts import render
from django.views.generic import ListView
from .models import Card, BodyContent
from django.views.decorators.http import require_GET

class BodyListView(ListView):
    model = Card
    queryset = Card.objects.all().order_by("id")
    template_name = 'body/body.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        body_list = BodyContent.objects.all()
        if body_list.exists():
            for body in body_list:
                # Default (home) page support only
                if body.page is None or body.page == '':
                    context['body_data'] += body
        return context
   
@require_GET
def body_detail(request):
    body_list = []
    card_content = Card.objects.all()
    body_content = BodyContent.objects.all()
    if card_content.exists():
        for card in card_content:
            if card.page == request.path.strip('/'):
                body_list += [card]
    if body_content.exists():
        for body in body_content:
            if body.page == request.path.strip('/'):
                body_list += [body]
    if body_list:
        return render(request, 'body/body.html', context={'body_list': body_list})
    # Fall back to default (home) page if no matching content found
    return render(request, 'body/body.html')
