from django import forms

from .models import SuperAdmin, User, UserGroup, Object

class RawLoginForm(forms.Form):
	username	= forms.CharField(
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
	password	= forms.CharField(
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

class CreateUserForm(forms.ModelForm):
	# def __init__(self, *args,**kwargs):
	# 	choices = kwargs.pop("choices", None)
	# 	super(CreateUserForm, self).__init__(*args, **kwargs)
	# 	self.fields['group'].queryset = UserGroup.objects.all()

	username	= forms.CharField(
						label='Username',
						required='True',
						widget=forms.TextInput(
							attrs={
								"class": "form-control",
								"autofocus": ""
							}
						)
					)
	password	= forms.CharField(
						label='Password',
						widget=forms.PasswordInput(
							attrs={
								"class": "form-control"
							}
						)
					)
	group		= forms.ModelChoiceField(		
						label='User Group',
						required='True',
						queryset = UserGroup.objects.all()
					)
	
	class Meta:
		model = User
		fields = [
			'username',
			'password',
			'group',
		]

class CreateGroupForm(forms.ModelForm):
	groupname	= forms.CharField(
						label='Group Name',
						required='True',
						widget=forms.TextInput(
							attrs={
								"class": "form-control",
								"autofocus": ""
							}
						)
					)

	class Meta:
		model = UserGroup
		fields = [
			'groupname',
		]

class EditGroupForm(forms.ModelForm):
	groupname	= forms.CharField(
						label='Group Name',
						required='True',
						widget=forms.TextInput(
							attrs={
								"class": "form-control edit-name",
								"autofocus": ""
							}
						)
					)

	class Meta:
		model = UserGroup
		fields = [
			'groupname',
		]

class CreateObjectForm(forms.ModelForm):
	username	= forms.CharField(
						label='Username',
						required='True',
						widget=forms.TextInput(
							attrs={
								"class": "form-control",
								"autofocus": ""
							}
						)
					)
	password	= forms.CharField(
						label='Password',
						widget=forms.PasswordInput(
							attrs={
								"class": "form-control"
							}
						)
					)
	group		= forms.ModelChoiceField(		
						label='Group',
						required='True',
						queryset = UserGroup.objects.all()
					)
	
	class Meta:
		model = Object
		fields = [
			'username',
			'password',
			'group',
		]