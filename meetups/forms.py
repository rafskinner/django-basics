from django import forms

from meetups.models import Participant


class RegistrationForm(forms.Form):
    email = forms.EmailField(label='Your email')


# class RegistrationForm(forms.ModelForm):
#     class Meta:
#         model = Participant
#         fields = ['email']
