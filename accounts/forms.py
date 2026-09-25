from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

  class Meta:
    model = CustomUser
    fields = ('email', 'username')  # Explicitly declare fields here

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    # Make username field optional so the system can auto-generate it if left blank
    self.fields['username'].required = False
    self.fields['username'].help_text = (
        'Optional. Leave blank to auto-generate a username.'
    )

    # Add Bootstrap styling to form fields
    for field_name, field in self.fields.items():
      field.widget.attrs['class'] = 'form-control'


class CustomAuthenticationForm(AuthenticationForm):
  username = forms.EmailField(
      label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'})
  )

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['password'].widget.attrs['class'] = 'form-control'