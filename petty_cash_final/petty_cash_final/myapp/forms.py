from django import forms
from .models import Signup


# creating a form
class SignupForm(forms.ModelForm):

	# create meta class
	class Meta:
		# specify model to be used
		model = Signup

		# specify fields to be used
		fields = '__all__'