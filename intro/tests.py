from django.test import TestCase
from django.contrib.auth import authenticate, login
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.http import HttpRequest

from intro.models import Intro

### --- Intro model testing
class TestIntro(TestCase):
    def test_model_properties(self):
        intro = Intro.objects.create(bgcolor="#123456", active=True)

        self.assertEqual(intro.bgcolor, "#123456")
        self.assertEqual(intro.active, True)

### --- Tinymce image upload testing
class TestTinymceUploadImage(TestCase):
    def setUp(self):
        request = HttpRequest()
        user = authenticate(request, username='admin', password='password')
        if user:
            # Manually attach the user to the client session
            self.client.force_login(user)

    def test_image_upload_as_superuser(self):
        image_content = b'GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
        test_image = SimpleUploadedFile('test.gif', image_content, content_type='image/gif')

        response = self.client.post(reverse('tinymce_upload_image'), {'image': test_image})
        self.assertEqual(response.status_code, 301) # Expect redirect on success (HTTP->HTTPS)
     
