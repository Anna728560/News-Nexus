from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from newspaper_agency.models import Newspaper, Redactor


class RedactorForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Redactor
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "years_of_experience",
        )


class NewspaperForm(forms.ModelForm):
    publishers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Newspaper
        fields = "__all__"


# class RedactorCreationForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = Redactor
#         fields = UserCreationForm.Meta.fields + (
#             "years_of_experience",
#             "first_name",
#             "last_name",
#         )
