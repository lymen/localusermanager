from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

from superadmin.models import Account, AccountChangeLog
from .forms import RawAccountRegisterForm

# Create your views here.
def account_register(request):
	registerform = RawAccountRegisterForm()
	response = True
	message = ""

	if request.method=='POST':
		registerform = RawAccountRegisterForm(request.POST)
		
		if registerform.is_valid():
			username = registerform.cleaned_data['username']
			password = registerform.cleaned_data['password']

			try:
				account = Account.objects.get(username=username)
				if (check_password(password, account.password)):
					message = "Password unchanged."
				else:
					print("Need to update password")
					raise Exception("Need to update password!")
			except:
				try:
					account = Account.objects.get(username=username)
					account.password = make_password(password, None, 'pbkdf2_sha256')
					account.save()

					changelog = AccountChangeLog(username=account, password=account.password)
					changelog.save()

					registerform = RawAccountRegisterForm()
					message = "Password updated."
				except Account.DoesNotExist:
					response = False
					registerform = RawAccountRegisterForm()

	context = {
		'register_form': registerform,
		'response': response,
		'message': message
	}
	return render(request, "account_register.html", context)