from django.test import TestCase, RequestFactory
from django.db import models
from .models import Card, CardSide, BodyContent
from .views import BodyListView, body_detail, dynamic_page_router
from django.urls import reverse
from http import HTTPStatus
from core.views import tinymce_upload_image

### --- Card, CardSide models testing
class CardTest(TestCase):
    def test_model_properties(self):
        card = Card.objects.create(box=1, active=True)
        front = CardSide.objects.create(card=card, is_front=True)
        back = CardSide.objects.create(card=card, is_front=False)
           
        self.assertEqual(card.box, 1)
        self.assertIsInstance(front, CardSide, "front should be of type CardSide")
        self.assertIsInstance(back, CardSide, "back should be of type CardSide" )
        self.assertEqual(front.is_front, True)
        self.assertEqual(back.is_front, False)
        self.assertEqual(card.active, True)
    
    def test_foreign_key_definition(self):
        field = CardSide._meta.get_field('card')
        
        self.assertIsInstance(field, models.ForeignKey)
        self.assertEqual(field.related_model, Card)

### --- BodyContent model testing  
class TestBodyContent(TestCase):
    def test_model_properties(self):
        body = BodyContent.objects.create(bgcolor="#123456", active=True)

        self.assertEqual(body.bgcolor, "#123456")
        self.assertEqual(body.active, True)

### --- BodyViews testing
class TestBodyViews(TestCase):
    def test_get_default_list(self):
        # Create some Card and BodyContent instances
        card1 = Card.objects.create(box=1, active=True)
        card2 = Card.objects.create(box=1, active=True, page='test')
        body1 = BodyContent.objects.create(active=True)
        body2 = BodyContent.objects.create(active=True, page='test')

        from .views import get_default_list

        # Test get_default_list with Card queryset
        card_queryset = get_default_list(Card.objects.all())
        self.assertIn(card1, card_queryset)
        self.assertNotIn(card2, card_queryset)

        # Test get_default_list with BodyContent queryset
        body_queryset = get_default_list(BodyContent.objects.all())
        self.assertIn(body1, body_queryset)
        self.assertNotIn(body2, body_queryset)

    ### --- body_detail view testing
    def test_body_detail_view(self):
        # Create a Card and BodyContent with specific page
        card = Card.objects.create(box=1, active=True, page='test')
        body = BodyContent.objects.create(active=True, page='test')

        # Create a request to the body_detail view
        factory = RequestFactory()
        request = factory.get('/test/')

        # Call the view
        response = body_detail(request)

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, HTTPStatus.OK)


    ### --- dynamic_page_router view testing
    def test_dynamic_page_router(self):
        # Create a BodyContent with specific page
        body = BodyContent.objects.create(active=True, page='test')

        # Create a request to the dynamic_page_router view
        factory = RequestFactory()
        request = factory.get('/test/')

        # Call the view
        response = dynamic_page_router(request, slug='test')

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, HTTPStatus.OK)

  
