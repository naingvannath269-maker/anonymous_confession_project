from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        field = ('email', 'username')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make username field optional in html
        self.fields['username'].required = False
        self.fields['username'].help_text = ('Optional. Leave blank to auto-generate a username.')

        # Add Bootstrap styling to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class CustomAuthenticationForm(AuthenticationForm):
  # Override default to use email instead of username for login
  username = forms.EmailField(
      label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'})
  )

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['password'].widget.attrs['class'] = 'form-control'
