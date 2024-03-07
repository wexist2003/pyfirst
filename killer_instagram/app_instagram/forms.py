from django.forms import ModelForm, ImageField, CharField, FileInput, TextInput, Textarea

from .models import Picture


class PictureForm(ModelForm):
    description = CharField(
        max_length=150, widget=TextInput(attrs={"class": "form-control"})
    )
    path = ImageField(widget=FileInput(attrs={"class": "form-control"}))
    additional_description = CharField(max_length=500, widget=Textarea(attrs={"class": "form-control"}))  # Поле для дополнительного текстового описания
    tags = CharField(max_length=100, required=False, widget=TextInput(attrs={"class": "form-control"}))  # Поле для списка тегов


    class Meta:
        model = Picture
        fields = ["description", "additional_description", "tags", "path"]
