from django import forms

class RawLoginForm(forms.Form):
	username		= forms.CharField(
						label='',
						required='True',
						widget=forms.TextInput(
								attrs={
									"placeholder": "Username",
									"id": "inputEmail",
									"class": "form-control",
									"autofocus": ""
								}
							)
						)
	password		= forms.CharField(
						label='',
						required='True',
						widget=forms.PasswordInput(
								attrs={
									"placeholder": "Password",
									"id": "inputPassword",
									"class": "form-control"
								}
							)
						)
