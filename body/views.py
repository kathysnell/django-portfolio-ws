from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from .models import Card, BodyContent
from django.views.decorators.http import require_GET

def get_default_list(list):
    queryset = []
    if list.exists():
        for item in list:
            # Default (home) page support only
            if item.page is None or item.page == '':
                queryset += [item]
    return queryset

class BodyListView(ListView):
    model = Card
    template_name = 'body/body.html'

    def get_queryset(self):
        # Only return default (home) page content for the list view
        return get_default_list(Card.objects.all().order_by("id"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        body_list = get_default_list(BodyContent.objects.all())
        if body_list:
            context['body_data'] = body_list
        card_list = get_default_list(Card.objects.all())
        if card_list:
            context['card_list'] = card_list
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

def dynamic_page_router(request, slug):
    # This only runs when a user actually visits a URL, required for postgres
    slug = slug.strip('/')
    link = get_object_or_404(BodyContent, page=slug)
    if link:
        return body_detail(request)
    return render(request, 'body/body.html', context={'link': link})
