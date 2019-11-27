from django import forms
from django.core.validators import FileExtensionValidator


class ImageForm(forms.Form):
    images = forms.FileField(
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif']),
        ],
        widget=forms.FileInput(attrs={"multiple": True})
    )
