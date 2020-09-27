from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import SuperAdmin, User, UserGroup
from .forms import RawLoginForm, CreateUserForm, CreateGroupForm, CreateObjectForm
from .forms import EditGroupForm

# Create your views here.
def superadmin_login(request):
	if request.session.get('adminuser'):
		return redirect('superadmin:superadmin-user')

	login = RawLoginForm()
	response = True

	if request.method=='POST':
		login = RawLoginForm(request.POST)
		
		if login.is_valid():
			username = login.cleaned_data['username']
			password = login.cleaned_data['password']

			try:
				superadmin = SuperAdmin.objects.get(username=username, password=password)
				login = RawLoginForm()
				request.session['adminuser'] = superadmin.username
				return redirect('superadmin:superadmin-user')
			except SuperAdmin.DoesNotExist:
				response = False
				login = RawLoginForm()

	context = {
		'login_form': login,
		'response': response
	}
	return render(request, "superadmin_login.html", context)

def superadmin_user(request):
	# Initial Check Begin
	username = request.session.get('adminuser')
	if not username:
		return redirect('superadmin:superadmin-login')

	if request.method=='POST' and 'logout' in request.POST:
		print("Logout")
		return superadmin_logout(request)
	# Initial Check End

	createuser = CreateUserForm()

	# Create User Begin
	if request.method=='POST' and 'createuser_form' in request.POST:
		createuser = CreateUserForm(request.POST or None)
		if createuser.is_valid():
			# createuser.save()
			createuser = CreateUserForm()
	# Create User End

	userlist = User.objects.all()
	context = {
		'username': username,
		'createuser_form': createuser,
		'user_list': userlist
	}

	return render(request, "superadmin_user.html", context)

def superadmin_group(request):
	# Initial Check Begin
	username = request.session.get('adminuser')
	if not username:
		return redirect('superadmin:superadmin-login')

	if request.method=='POST' and 'logout' in request.POST:
		print("Logout")
		return superadmin_logout(request)
	# Initial Check End

	creategroup = CreateGroupForm()
	editgroup = EditGroupForm()

	# Create Group Begin
	if request.method=='POST' and 'creategroup_form' in request.POST:
		creategroup = CreateGroupForm(request.POST or None)
		if creategroup.is_valid():
			# creategroup.save()
			creategroup = CreateGroupForm()
	# Create Group End

	# Edit Group Begin
	if request.method=='POST' and 'editgroup_form' in request.POST:
		editgroup = EditGroupForm(request.POST or None)
		print(editgroup)
		if editgroup.is_valid():
			print('editgroup')
			# obj = UserGroup.objects.get(id=editgroup.id)
			obj.groupname = editgroup.cleaned_data['groupname']
			obj.save()
			editgroup = EditGroupForm()
	# Edit Group End

	message = "None"
	result = True
	grouplist = UserGroup.objects.all()
	context = {
		'username': username,
		'creategroup_form': creategroup,
		'group_list': grouplist,
		'message': message,
		'result': result
	}

	return render(request, "superadmin_group.html", context)

def superadmin_editgroup(request, id):
	# Initial Check Begin
	username = request.session.get('adminuser')
	if not username:
		return redirect('superadmin:superadmin-login')

	if request.method=='POST' and 'logout' in request.POST:
		print("Logout")
		return superadmin_logout(request)
	# Initial Check End

	obj = UserGroup.objects.get(id=id)
	editgroup = EditGroupForm(instance=obj)

	# Edit Group Begin
	if request.method=='POST' and 'editgroup_form' in request.POST:
		editgroup = EditGroupForm(request.POST or None)

		if editgroup.is_valid():
			obj.groupname = editgroup.cleaned_data['groupname']
			obj.save()
			editgroup = EditGroupForm()
			return redirect('superadmin:superadmin-group')
	# Edit Group End

	context = {
		'username': username,
		'editgroup_form': editgroup,
	}

	return render(request, "superadmin_editgroup2.html", context)

def validate_username(request, id):
	print('validate entry')
	obj = UserGroup.objects.get(id=id)
	data = dict();
	if request.method=='POST':
		form = EditGroupForm(instance=obj)
		if form.is_valid():
			print('validate')
			obj.groupname = form.cleaned_data['groupname']
			form.save()
			data['form_is_valid'] = TRUE
		else:
			data['form_is_valid'] = FALSE
	else:
		form = EditGroupForm(instance=obj)

	context = {
		'editgroup_form': form,
		'editid': id
	}

	data['html_form'] = render_to_string('superadmin_editgroup.html', context, request=request)
	print('validate end')
	return JsonResponse(data)

def superadmin_object(request):
	# Initial Check Begin
	username = request.session.get('adminuser')
	if not username:
		return redirect('superadmin:superadmin-login')

	if request.method=='POST' and 'logout' in request.POST:
		print("Logout")
		return superadmin_logout(request)
	# Initial Check End

	createobject = CreateObjectForm()

	# Create Object Begin
	if request.method=='POST' and 'createobject_form' in request.POST:
		# createobject = CreateObjectForm(request.POST or None)
		if createobject.is_valid():
			# createobject.save()
			createobject = CreateObjectForm()
	# Create Object End

	context = {
		'username': username,
		'createobject_form': createobject
	}

	return render(request, "superadmin_object.html", context)

def superadmin_logout(request):
	username = request.session.get('adminuser')
	if username and request.method=='POST' and 'logout' in request.POST:
		print("Logout Button Clicked")
		del request.session['adminuser']
		return redirect('superadmin:superadmin-login')
	
	print("Logout Button Unclicked")
	return redirect('superadmin:superadmin-user')