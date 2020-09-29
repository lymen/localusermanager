from django.shortcuts import render
from django.utils import timezone

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
				account = Account.objects.get(username=username, password=password)
				message = "Password unchanged."
			except Account.DoesNotExist:
				try:
					account = Account.objects.get(username=username)
					account.password = password
					account.save()

					changelog = AccountChangeLog(username=account, password=password)
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