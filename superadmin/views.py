from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import make_password, check_password

from .models import SuperAdmin, User, UserGroup, Account, AccountChangeLog
from .forms import RawLoginForm, CreateUserForm, GroupForm, CreateAccountForm
from .forms import EditUserForm, EditAccountForm

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

	result = True
	message = ""
	createuser = CreateUserForm()
	errorform = CreateUserForm()
	edituser = EditUserForm()

	# Create User Begin
	if request.method=='POST' and 'createuser_form' in request.POST:
		createuser = CreateUserForm(request.POST or None)
		print(createuser.errors.as_data())
		if createuser.is_valid():
			createuser.save()
			message = "Successfully created new user."
		else:
			result = False
			errorform = createuser

		createuser = CreateUserForm()
	# Create User End

	# Edit User Begin
	if request.method=='POST' and 'edit_form' in request.POST:
		edituser = EditUserForm(request.POST or None)
		# edituser = PasswordChangeForm(request.user, request.POST)
		print(edituser.errors.as_data())
		if edituser.is_valid():
			edituser.save();
			message = "New user was created."
		else:
			obj = User.objects.get(id=request.session.get('editid'))
			obj.password = edituser.cleaned_data['password']
			obj.group.set(edituser.cleaned_data['group'])
			obj.save()
			del request.session['editid']
			message = "Successfully updated the user details."

		edituser = EditUserForm()
	# Edit User End

	# Delete User Begin
	if request.method=='POST' and 'delete_form' in request.POST:
		try:
			obj = User.objects.get(id=request.session.get('deleteid'))
			obj.delete()
			del request.session['deleteid']
			message = "Successfully deleted the user details."
		except User.DoesNotExist:
			return redirect('superadmin:superadmin-user')
	# Delete User End

	userlist = User.objects.all()
	context = {
		'username': username,
		'createuser_form': createuser,
		'user_list': userlist,
		'result': result,
		'message': message,
		'errorform' : errorform
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
	errorform = GroupForm()
	editgroup = GroupForm()
	result = True
	message = ""

	# Create Group Begin
	if request.method=='POST' and 'creategroup_form' in request.POST:
		creategroup = GroupForm(request.POST or None)
		if creategroup.is_valid():
			creategroup.save()
			message = "Successfully created new group."
		else:
			result = False
			errorform = creategroup

		creategroup = GroupForm()
	# Create Group End

	# Edit Group Begin
	if request.method=='POST' and 'edit_form' in request.POST:
		editgroup = GroupForm(request.POST or None)

		if editgroup.is_valid():
			obj = UserGroup.objects.get(id=request.session.get('editid'))
			obj.groupname = editgroup.cleaned_data['groupname']
			obj.save()
			del request.session['editid']
			message = "Successfully updated the group name."
		else:
			result = False
			errorform = creategroup

		editgroup = GroupForm()
	# Edit Group End

	# Delete Group Begin
	if request.method=='POST' and 'delete_form' in request.POST:
		try:
			obj = UserGroup.objects.get(id=request.session.get('deleteid'))
			obj.delete()
			del request.session['deleteid']
			message = "Successfully deleted the group."
		except UserGroup.DoesNotExist:
			return redirect('superadmin:superadmin-group')
	# Delete Group End

	grouplist = UserGroup.objects.all()
	context = {
		'username': username,
		'creategroup_form': creategroup,
		'group_list': grouplist,
		'message': message,
		'result': result,
		'errorform': errorform
	}

	return render(request, "superadmin_group.html", context)

def superadmin_account(request):
	# Initial Check Begin
	username = request.session.get('adminuser')
	if not username:
		return redirect('superadmin:superadmin-login')

	if request.method=='POST' and 'logout' in request.POST:
		print("Logout")
		return superadmin_logout(request)
	# Initial Check End

	result = True
	message = ""
	errorform = CreateAccountForm()
	createaccount = CreateAccountForm()
	editaccount = EditAccountForm()

	# Create Account Begin
	if request.method=='POST' and 'createaccount_form' in request.POST:
		createaccount = CreateAccountForm(request.POST or None)
		print(createaccount.errors.as_data())
		if createaccount.is_valid():
			createaccount.save()
			message = "Successfully created new Account."
			try:
				account = Account.objects.get(username=createaccount.cleaned_data['username'])
				changelog = AccountChangeLog(username=account, password=createaccount.cleaned_data['password'])
				changelog.save()
			except Account.DoesNotExist:
				print("here")
				changelog = ""
		else:
			result = False
			errorform = createaccount

		createaccount = CreateAccountForm()
	# Create Account End

	# Edit Account Begin
	if request.method=='POST' and 'edit_form' in request.POST:
		editaccount = EditAccountForm(request.POST or None)
		# editaccount = PasswordChangeForm(request.account, request.POST)
		print(editaccount.errors.as_data())
		if editaccount.is_valid():
			editaccount.save();
			message = "New Account was created."
		else:
			obj = Account.objects.get(id=request.session.get('editid'))
			obj.password = editaccount.cleaned_data['password']
			obj.group.set(editaccount.cleaned_data['group'])
			obj.save()
			del request.session['editid']
			message = "Successfully updated the Account details."
		
		editaccount = EditAccountForm()
	# Edit Account End

	# Delete Account Begin
	if request.method=='POST' and 'delete_form' in request.POST:
		try:
			obj = Account.objects.get(id=request.session.get('deleteid'))
			obj.delete()
			del request.session['deleteid']
			message = "Successfully deleted the Account details."
		except Account.DoesNotExist:
			return redirect('superadmin:superadmin-account')
	# Delete Account End

	accountlist = Account.objects.all()
	context = {
		'username': username,
		'createaccount_form': createaccount,
		'account_list': accountlist,
		'result': result,
		'message': message,
		'errorform' : errorform
	}

	return render(request, "superadmin_account.html", context)

def superadmin_logout(request):
	username = request.session.get('adminuser')
	if username and request.method=='POST' and 'logout' in request.POST:
		print("Logout Button Clicked")
		del request.session['adminuser']
		return redirect('superadmin:superadmin-login')
	
	print("Logout Button Unclicked")
	return redirect('superadmin:superadmin-user')

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

def superadmin_editaccount(request, id):
	request.session['editid'] = id
	obj = Account.objects.get(id=id)
	data = dict();

	form = EditAccountForm(instance=obj)

	context = {
		'edit_form': form,
		'module': 'Account'
	}

	data['html_form'] = render_to_string('superadmin_edit.html', context, request=request)
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

def superadmin_deleteaccount(request, id):
	request.session['deleteid'] = id
	data = dict();

	form = EditAccountForm(instance=Account.objects.get(id=id))
	context = {
		'form': form,
		'module': 'Account'
	}

	data['html_form'] = render_to_string('superadmin_delete.html', context, request=request)
	return JsonResponse(data)