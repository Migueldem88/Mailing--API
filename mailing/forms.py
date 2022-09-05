from django import forms
from .models import Article, Subscriber


emails = Subscriber.objects.all().values("email").distinct()
EMAIL_CHOICES = []
for i in emails:
    EMAIL_CHOICES.append([i.get('email'),i.get('email')])


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    #to = forms.EmailField()
    comments = forms.CharField(required=False,
    widget=forms.Textarea)
    to = forms.MultipleChoiceField(choices=EMAIL_CHOICES)

class SubscriberForm(forms.Form):
    email = forms.EmailField(label='Your email',
                             max_length=100,
                             widget=forms.EmailInput(attrs={'class':'form-control'}))
