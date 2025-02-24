from django import forms
from .models import Target

class TargetForm(forms.ModelForm):
    class Meta:
        model = Target
        fields = ['name', 'email', 'department']

class TargetUploadForm(forms.Form):
    file = forms.FileField()
