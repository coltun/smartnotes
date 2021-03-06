from django import forms  
from django.contrib.auth.models import User  
from django.contrib.auth.forms import AuthenticationForm, UsernameField


class CustomLoginForm(AuthenticationForm):
    username = UsernameField(
        label='Email',)
    
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class UserRegistrationForm(forms.ModelForm):
	password = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ['email']

	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password'] != cd['password2']:
			raise forms.ValidationError('Passwords don\'t match.')
		return cd['password2']

	def __init__(self, *args, **kwargs):
		super(UserRegistrationForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'

