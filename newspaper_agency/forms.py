from django.contrib.auth.forms import UserCreationForm
from django import forms

from newspaper_agency.models import (
    Redactor,
    Newspaper, Topic
)


class RedactorForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Redactor
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "years_of_experience",
        )


class NewspaperForm(forms.ModelForm):
    class Meta:
        model = Newspaper
        fields = ("title", "content", "topic")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "topic": forms.CheckboxSelectMultiple(attrs={"class": "form-control"}),
            # Select(attrs={"class": "form-control"})
        }
