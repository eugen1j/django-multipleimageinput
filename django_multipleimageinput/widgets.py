from pathlib import Path

from django.forms import Widget


class MultipleImageInput(Widget):
    template_name = 'django_multipleimageinput/multipleimageinput.html'

    def __init__(self, upload_url: str, media_prefix: Path, attrs=None):
        super().__init__(attrs)
        self._upload_url = upload_url
        self._media_prefix = media_prefix

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['image_list'] = value.split(',') if value != '' else []
        context['widget']['upload_url'] = self._upload_url
        context['widget']['media_prefix'] = self._media_prefix
        return context

    class Media:
        css = {"all": ["django_multipleimageinput/multipleimageinput.css"]}
        js = ["django_multipleimageinput/multipleimageinput.js"]
