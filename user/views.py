from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password

from superadmin.models import User, UserGroup, Account, AccountChangeLog
from .forms import RawLoginForm

# Create your views here.
def user_login(request):
	if request.session.get('user'):
		return redirect('user:user-home')

	login = RawLoginForm()
	response = True

	if request.method=='POST':
		login = RawLoginForm(request.POST)
		
		if login.is_valid():
			username = login.cleaned_data['username']
			password = login.cleaned_data['password']

			try:
				user = User.objects.get(username=username)
				if check_password(password, user.password):
					print("Success")
					login = RawLoginForm()
					request.session['user'] = username
					return redirect('user:user-home')
				else:
					response = False
					login = RawLoginForm()
			except User.DoesNotExist:
				response = False
				login = RawLoginForm()

	context = {
		'login_form': login,
		'response': response
	}
	return render(request, "user_login.html", context)

def user_home(request):
	changelog = ""
	username = request.session.get('user')

	if not username:
		return redirect('user:user-login')

	if request.method=='POST' and 'logout' in request.POST:
		print("Logout")
		return user_logout(request)

	if request.method=='POST' and 'search_form' in request.POST:
		print(request.POST.get("searchkey"))
		searchkey = request.POST.get("searchkey")

		try:
			userdata = User.objects.get(username=username)
			grouplist = userdata.group.all().values_list('id', flat='True')

			try:
				accountid = Account.objects.filter(username=searchkey, group__id__in=grouplist).values_list('id', flat='True').distinct()

				for id in accountid.iterator():
					try:
						accountdata = Account.objects.get(id=id)
						try:
							changelog = AccountChangeLog.objects.filter(username=accountdata).order_by('-modified')
						except AccountChangeLog.DoesNotExist:
							changelog = ""
					except Account.DoesNotExist:
						changelog = ""

			except Account.DoesNotExist:
				changelog = ""
		except User.DoesNotExist:
			changelog = ""

	context = {
		'username': username,
		'changelog': changelog
	}

	return render(request, "user_home.html", context)

def user_logout(request):
	username = request.session.get('user')
	if username and request.method=='POST' and 'logout' in request.POST:
		print("Logout Button Clicked")
		del request.session['user']
		return redirect('user:user-login')
	
	print("Logout Button Unclicked")
	return redirect('user:user-home')