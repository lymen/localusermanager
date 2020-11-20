from django import forms

from .models import SuperAdmin, User, UserGroup, Account, CSV

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

class ChangePasswordForm(forms.Form):
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
	oldpassword	= forms.CharField(
					label='',
					required='True',
					widget=forms.PasswordInput(
							attrs={
								"placeholder": "Old Password",
								"id": "inputPassword",
								"class": "form-control"
							}
						)
					)
	newpassword	= forms.CharField(
					label='',
					required='True',
					widget=forms.PasswordInput(
							attrs={
								"placeholder": "New Password",
								"id": "inputPassword",
								"class": "form-control"
							}
						)
					)

class CreateUserForm(forms.ModelForm):
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
	group		= forms.ModelMultipleChoiceField(
						label='User Group',
						required='True',
						widget=forms.SelectMultiple(),
						queryset = UserGroup.objects.all()
					)
	
	class Meta:
		model = User
		fields = [
			'username',
			'password',
			'group',
		]

class EditUserForm(forms.ModelForm):
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
						label='Enter New Password',
						widget=forms.PasswordInput(
							attrs={
								"class": "form-control"
							}
						)
					)
	group		= forms.ModelMultipleChoiceField(
						label='User Group',
						required='True',
						widget=forms.SelectMultiple(),
						queryset = UserGroup.objects.all()
					)
	
	class Meta:
		model = User
		fields = [
			'username',
			'password',
			'group',
		]

class GroupForm(forms.ModelForm):
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

class CreateAccountForm(forms.ModelForm):
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
	group		= forms.ModelMultipleChoiceField(
						label='User Group',
						required='True',
						widget=forms.SelectMultiple(),
						queryset = UserGroup.objects.all()
					)
	
	class Meta:
		model = Account
		fields = [
			'username',
			'password',
			'group',
		]

class EditAccountForm(forms.ModelForm):
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
						label='Enter New Password',
						widget=forms.PasswordInput(
							attrs={
								"class": "form-control"
							}
						)
					)
	group		= forms.ModelMultipleChoiceField(
						label='User Group',
						required='True',
						widget=forms.SelectMultiple(),
						queryset = UserGroup.objects.all()
					)
	
	class Meta:
		model = Account
		fields = [
			'username',
			'password',
			'group',
		]

class CSVModelForm(forms.ModelForm):
	filename	= forms.FileField(label='')

	class Meta:
		model = CSV
		fields = [
			'filename'
		]