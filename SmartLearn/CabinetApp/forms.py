from django import forms
from CabinetApp.models import Record, Cabinet
from ChatApp.models import User


class RecordsForms(forms.ModelForm):
    title = forms.CharField()
    url = forms.URLField()

    class Meta:
        model = Record
        fields = ['title', 'url', 'cabinet']


class SendEmailForm(forms.Form):
    user = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple(), required=False)
    subject = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Тема',
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'cols': 80,
        'rows': 20,
        'class': 'form-control',
    }), required=False)
    is_lesson = forms.BooleanField(required=False)
