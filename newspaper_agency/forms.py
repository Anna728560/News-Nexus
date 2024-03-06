from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from newspaper_agency.models import (
    Redactor,
    Newspaper,
)


class RedactorCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Redactor
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "years_of_experience",
        )


class RedactorLoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class NewspaperForm(forms.ModelForm):
    class Meta:
        model = Newspaper
        fields = ("title", "content", "topic")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "topic": forms.Select(attrs={"class": "form-control"}),
        }


class TopicSearchForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by topic"
            }
        )
    )
