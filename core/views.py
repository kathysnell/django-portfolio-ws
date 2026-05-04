import os
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from .utils import save_webp

@staff_member_required
@csrf_exempt
def tinymce_upload_image(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file_obj = request.FILES['file']     
        file_path = os.path.join('tinymce/upload_images', file_obj.name)
        filename = default_storage.save(file_path, file_obj)
        file_url = default_storage.url(filename)
        save_webp(file_path)
        return JsonResponse({'location': file_url})    
    return JsonResponse({'error': 'Invalid request'}, status=400)
