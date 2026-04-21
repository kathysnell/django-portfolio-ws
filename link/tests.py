from django.test import TestCase

from link.models import Link, LinkBar

### --- Link, LinkBar models testing
class TestLinkModels(TestCase):
    def test_model_properties(self):
        link = Link.objects.create(text="Test Link", url="https://example.com", active=True)
        link_bar = LinkBar.objects.create(position='pre_header', justify='center', active=True)

        self.assertEqual(link.text, "Test Link")
        self.assertEqual(link.url, "https://example.com")
        self.assertEqual(link.active, True)

        self.assertEqual(link_bar.position, 'pre_header')
        self.assertEqual(link_bar.justify, 'center')
        self.assertEqual(link_bar.active, True)

    

    
