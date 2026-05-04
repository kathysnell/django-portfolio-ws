# storage.py
from django.core.files.storage import FileSystemStorage

class NoSuffixStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        return name
