from django.shortcuts import render, redirect, get_object_or_404

from superadmin.models import User, UserGroup
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
				user = User.objects.get(username=username, password=password)
				login = RawLoginForm()
				request.session['user'] = username
				return redirect('user:user-home')
			except User.DoesNotExist:
				response = False
				login = RawLoginForm()

	context = {
		'login_form': login,
		'response': response
	}
	return render(request, "user_login.html", context)

def user_home(request):
	userdata = {}
	username = request.session.get('user')
	if not username:
		return redirect('user:user-login')

	if request.method=='POST' and 'logout' in request.POST:
		print("Logout")
		return user_logout(request)

	try:
		userdata = User.objects.get(username=username)
		response = {
			'username': userdata.username,
			'password': userdata.password,
			'group': userdata.group
		}
	except User.DoesNotExist:
		# not possible
		userdata = {}

	context = {
		'response': response
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