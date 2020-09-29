from django.urls import path
from .views import (
	superadmin_login,
	superadmin_user,
	superadmin_group,
	superadmin_account,
	superadmin_edituser,
	superadmin_editgroup,
	superadmin_editaccount,
	superadmin_deleteuser,
	superadmin_deletegroup,
	superadmin_deleteaccount
	)

app_name = 'superadmin'
urlpatterns = [
    # path('product/', product_detail_view),
    path('', superadmin_login, name='superadmin-login'),
    path('user', superadmin_user, name='superadmin-user'),
    path('user/<int:id>/edit/', superadmin_edituser, name='superadmin-edituser'),
    path('user/<int:id>/delete/', superadmin_deleteuser, name='superadmin-deleteuser'),
    path('group', superadmin_group, name='superadmin-group'),
    path('group/<int:id>/edit/', superadmin_editgroup, name='superadmin-editgroup'),
    path('group/<int:id>/delete/', superadmin_deletegroup, name='superadmin-deletegroup'),
    path('account', superadmin_account, name='superadmin-account'),
    path('account/<int:id>/edit/', superadmin_editaccount, name='superadmin-editaccount'),
    path('account/<int:id>/delete/', superadmin_deleteaccount, name='superadmin-deleteaccount'),
]