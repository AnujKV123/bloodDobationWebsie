from django import forms
from App_Blood.models import *


class ContactusForm(forms.ModelForm):
    name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=100)
    subject = forms.CharField(max_length=50)
    message =forms.CharField(label="Message", widget=forms.Textarea(attrs={
        'class': 'form-control',
        'border':'none',
        'id': 'comm',
        'rows': 2,
        'cols': 40
    }))

    class Meta:
        model=Contactus
        fields=['name','email','subject','message']


class CommentForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(attrs={
        'class': 'form-control',
        'id': 'comm',
        'rows': 2,
        'cols': 40,
        'placeholder': "Enter  your Text here",
    }))

    class Meta:
        model = Comment
        fields = ['content']
