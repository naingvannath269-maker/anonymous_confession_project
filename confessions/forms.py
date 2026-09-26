from django import forms
from .models import Confession


class ConfessionForm(forms.ModelForm):
  class Meta:
    model = Confession
    fields = ['content']
    widgets = {
        'content': forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Type your confession here... (keep it kind)',
            }
        ),
    }