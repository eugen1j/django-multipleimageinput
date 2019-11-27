# Django MultipleImageInput

Widget for multiple image fields. Works good with PostgreSQL array fields.


## Example

In this example i use [crispy_forms](https://github.com/django-crispy-forms/django-crispy-forms)

settings.py

```python
import pathlib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MEDIA_URL = '/media/'
MEDIA_ROOT = pathlib.Path(BASE_DIR) / 'common' / 'media'
```

model.py

```python
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Product(models.Model):
    class Meta:
        db_table = 'product'
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    IMAGE_PATH = 'common/image/product'

    title = models.TextField('заголовок', null=True, blank=True)
    description = models.TextField('описание', null=True, blank=True)
    price = models.IntegerField('цена')
    youtube_url = models.URLField('видео youtube', null=True, blank=True)
    image_list = ArrayField(models.TextField("картинки"), default=list, verbose_name='картинки', blank=True)
```

view.py
```python
from settings import MEDIA_ROOT
from models import Product
import django_multipleimageinput

class UploadImageView(django_multipleimageinput.UploadImageView):
    media_root = MEDIA_ROOT
    image_path = Product.IMAGE_PATH
```
    
forms.py
```python
from django import forms
from models import Product
from django_multipleimageinput import MultipleImageInput
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Submit, Layout


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["title", "description", "price", "youtube_url", "image_list"]
        widgets = {
            "title": forms.TextInput(),
            "description": forms.Textarea(attrs={'rows': 4, 'cols': 15}),
            "image_list": MultipleImageInput(reverse_lazy('common:product/upload-image'), MEDIA_URL)
        }

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()

        self.helper.layout = Layout(
            'title',
            'description',
            'price',
            'youtube_url',
            'image_list',
            ButtonHolder(
                Submit('submit', 'Сохранить')
            )
        )
        super(ProductForm, self).__init__(*args, **kwargs)

```

urls.py
```python
from django.urls import path
from django.conf.urls.static import static as sttc
import views
import settings

app_name = 'common'

urlpatterns = [
    path('product/upload-image', views.UploadImageView.as_view(), name='product/upload-image'),
] + sttc(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

