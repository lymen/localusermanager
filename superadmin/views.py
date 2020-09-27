from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from .models import SuperAdmin, User, UserGroup, Object
from .forms import RawLoginForm, CreateUserForm, GroupForm, CreateObjectForm
from .forms import EditUserForm, EditObjectForm

# update_session_auth_hash(request, user)

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
	edituser = EditUserForm()

	# Create User Begin
	if request.method=='POST' and 'createuser_form' in request.POST:
		createuser = CreateUserForm(request.POST or None)
		print(createuser.errors.as_data())
		if createuser.is_valid():
			createuser.save()
		
		createuser = CreateUserForm()
	# Create User End

	# Edit User Begin
	if request.method=='POST' and 'edit_form' in request.POST:
		edituser = EditUserForm(request.POST or None)
		# edituser = PasswordChangeForm(request.user, request.POST)
		print(edituser.errors.as_data())
		if edituser.is_valid():
			edituser.save();
		else:
			obj = User.objects.get(id=request.session.get('editid'))
			obj.password = edituser.cleaned_data['password']
			obj.group = edituser.cleaned_data['group']
			obj.save()
			edituser = EditUserForm()
			del request.session['editid']
	# Edit User End

	# Delete User Begin
	if request.method=='POST' and 'delete_form' in request.POST:
		obj = User.objects.get(id=request.session.get('deleteid'))
		obj.delete()
		del request.session['deleteid']
	# Delete User End

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

	creategroup = GroupForm()
	editgroup = GroupForm()

	# Create Group Begin
	if request.method=='POST' and 'creategroup_form' in request.POST:
		creategroup = GroupForm(request.POST or None)
		if creategroup.is_valid():
			creategroup.save()
			creategroup = GroupForm()
	# Create Group End

	# Edit Group Begin
	if request.method=='POST' and 'edit_form' in request.POST:
		editgroup = GroupForm(request.POST or None)

		if editgroup.is_valid():
			obj = UserGroup.objects.get(id=request.session.get('editid'))
			obj.groupname = editgroup.cleaned_data['groupname']
			obj.save()
			editgroup = GroupForm()
			del request.session['editid']
	# Edit Group End

	# Delete Group Begin
	if request.method=='POST' and 'delete_form' in request.POST:
		obj = UserGroup.objects.get(id=request.session.get('deleteid'))
		obj.delete()
		del request.session['deleteid']
	# Delete Group End

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
	request.session['editid'] = id
	obj = UserGroup.objects.get(id=id)
	data = dict();

	form = GroupForm(instance=obj)

	context = {
		'edit_form': form,
		'module': 'Group'
	}

	data['html_form'] = render_to_string('superadmin_edit.html', context, request=request)
	return JsonResponse(data)

def superadmin_edituser(request, id):
	request.session['editid'] = id
	obj = User.objects.get(id=id)
	data = dict();

	form = EditUserForm(instance=obj)

	context = {
		'edit_form': form,
		'module': 'User'
	}

	data['html_form'] = render_to_string('superadmin_edit.html', context, request=request)
	return JsonResponse(data)

def superadmin_editobject(request, id):
	request.session['editid'] = id
	obj = Object.objects.get(id=id)
	data = dict();

	form = EditObjectForm(instance=obj)

	context = {
		'edit_form': form,
		'module': 'Object'
	}

	data['html_form'] = render_to_string('superadmin_edit.html', context, request=request)
	return JsonResponse(data)

def superadmin_deletegroup(request, id):
	request.session['deleteid'] = id
	data = dict();

	form = GroupForm(instance=UserGroup.objects.get(id=id))

	context = {
		'form': form,
		'module': 'Group'
	}

	data['html_form'] = render_to_string('superadmin_delete.html', context, request=request)
	return JsonResponse(data)

def superadmin_deleteuser(request, id):
	request.session['deleteid'] = id
	data = dict();

	form = EditUserForm(instance=User.objects.get(id=id))
	context = {
		'form': form,
		'module': 'User'
	}

	data['html_form'] = render_to_string('superadmin_delete.html', context, request=request)
	return JsonResponse(data)

def superadmin_deleteobject(request, id):
	request.session['deleteid'] = id
	data = dict();

	form = EditObjectForm(instance=Object.objects.get(id=id))
	context = {
		'form': form,
		'module': 'Object'
	}

	data['html_form'] = render_to_string('superadmin_delete.html', context, request=request)
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
	editobject = EditObjectForm()

	# Create Object Begin
	if request.method=='POST' and 'createobject_form' in request.POST:
		createobject = CreateObjectForm(request.POST or None)
		print(createobject.errors.as_data())
		if createobject.is_valid():
			createobject.save()
			createobject = CreateObjectForm()
	# Create Object End

	# Edit Object Begin
	if request.method=='POST' and 'edit_form' in request.POST:
		editobject = EditObjectForm(request.POST or None)
		# editobject = PasswordChangeForm(request.object, request.POST)
		print(editobject.errors.as_data())
		if editobject.is_valid():
			editobject.save();
		else:
			obj = Object.objects.get(id=request.session.get('editid'))
			obj.password = editobject.cleaned_data['password']
			obj.group = editobject.cleaned_data['group']
			obj.save()
			editobject = EditObjectForm()
			del request.session['editid']
	# Edit Object End

	# Delete Object Begin
	if request.method=='POST' and 'delete_form' in request.POST:
		obj = Object.objects.get(id=request.session.get('deleteid'))
		obj.delete()
		del request.session['deleteid']
	# Delete Object End

	objectlist = Object.objects.all()
	context = {
		'username': username,
		'createobject_form': createobject,
		'object_list': objectlist
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