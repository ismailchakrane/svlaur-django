from .models import User
from django import forms


class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'email', 'password','major','year_of_major',
                  'linkedin_link','place_of_work','job_title','year_of_graduate','is_graduate',
                  'is_admin')