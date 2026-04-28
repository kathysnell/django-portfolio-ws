import os
from io import BytesIO
from PIL import Image
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def save_webp(storage_path, quality=80):
    # Converts a Django Image file to WebP.
    if not default_storage.exists(storage_path):
        return
    try:
        # Verify file extension 
        ext = os.path.splitext(storage_path)[1].lower()
        if ext not in ['.jpg', '.jpeg', '.png']:
            return None
        with default_storage.open(storage_path) as f:
            img = Image.open(f)
            output = BytesIO()
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGBA")
            else:
                img = img.convert("RGB")
            img.save(output, format='WEBP', quality=80)
            
            webp_path = os.path.splitext(storage_path)[0] + '.webp'
            if not default_storage.exists(webp_path):
                default_storage.save(webp_path, ContentFile(output.getvalue()))
            return webp_path
    except Exception as e:
        print(f"exception: {e}")
        return None
