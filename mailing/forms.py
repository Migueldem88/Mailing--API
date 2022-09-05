from django import forms
from .models import Subscriber, Email
from django.forms import ModelForm

def mails():
    mails = Subscriber.objects.all().values("email").distinct()
    EMAIL_CHOICES = []
    for i in mails:
        EMAIL_CHOICES.append([i.get('email'),i.get('email')])
    return EMAIL_CHOICES


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    to = forms.MultipleChoiceField(choices=mails())
    #to = forms.EmailField()
    comments = forms.CharField(required=False,
    widget=forms.Textarea)


class SubscriberForm(forms.Form):
    email = forms.EmailField(label='Your email',
                             max_length=100,
                             widget=forms.EmailInput(attrs={'class':'form-control'}))

class EmailSendForm(ModelForm):
    to = forms.MultipleChoiceField(choices=mails())
    #to_another = forms.EmailField()
    attach = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta:
        model = Email
        fields=['subject','content',]
