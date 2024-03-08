from django.forms import ModelForm, ImageField, CharField, FileInput, TextInput, Textarea

from .models import Picture


class PictureForm(ModelForm):
    description = CharField(
        max_length=1000, widget=Textarea(attrs={"class": "form-control"})
    )
    path = ImageField(required=False, widget=FileInput(attrs={"class": "form-control"}))
    additional_description = CharField(max_length=100, widget=TextInput(attrs={"class": "form-control"}))  # Поле для дополнительного текстового описания
    tags = CharField(max_length=100, required=False, widget=TextInput(attrs={"class": "form-control"}))  # Поле для списка тегов


    class Meta:
        model = Picture
        fields = ["description", "additional_description", "tags", "path"]


class AuthorForm(ModelForm):
    description = CharField(
        max_length=100, widget=TextInput(attrs={"class": "form-control"})
    )
    born = CharField(
        max_length=100, widget=TextInput(attrs={"class": "form-control"})
    )    
    path = ImageField(required=False, widget=FileInput(attrs={"class": "form-control"}))
    additional_description = CharField(max_length=2000, widget=Textarea(attrs={"class": "form-control"}))  # Поле для дополнительного текстового описания
    tags = CharField(max_length=100, required=False, widget=TextInput(attrs={"class": "form-control"}))  # Поле для списка тегов


    class Meta:
        model = Picture
        fields = ["description", "born", "additional_description", "tags", "path"]