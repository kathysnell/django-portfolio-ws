from django.views.generic import ListView
from .models import Card, BodyContent


class BodyListView(ListView):
    model = Card
    queryset = Card.objects.all().order_by("id")
    template_name = 'body/body.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['body_data'] = BodyContent.objects.first()
        return context
