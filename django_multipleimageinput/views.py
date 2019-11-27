import json
import string
from pathlib import Path
from typing import List

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpRequest, JsonResponse
from django.utils.crypto import get_random_string
from django.views import generic
from .forms import ImageForm
from .file import Storage


class UploadImageView(generic.View):
    media_root = ''
    image_path = ''

    def post(self, request: HttpRequest):
        form = ImageForm(request.POST, request.FILES)
        paths = []
        if form.is_valid():
            # noinspection PyCallByClass, PyArgumentList
            images: List[InMemoryUploadedFile] = request.FILES.getlist('images')
            for image in images:
                name = get_random_string(32, string.hexdigits.lower()) + '.' + Path(
                    image.name).suffix[1:].lower()
                storage = Storage(str(Path(self.media_root) / self.image_path))
                path = storage.save(name, image)
                paths.append(str(Path(self.image_path) / path))

        return JsonResponse(paths, safe=False)
