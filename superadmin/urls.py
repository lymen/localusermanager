from django.urls import path
from .views import (
	superadmin_login,
	superadmin_user,
	superadmin_group,
	superadmin_object,
	superadmin_edituser,
	superadmin_editgroup,
	superadmin_editobject,
	superadmin_deleteuser,
	superadmin_deletegroup,
	superadmin_deleteobject
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
    path('object', superadmin_object, name='superadmin-object'),
    path('object/<int:id>/edit/', superadmin_editobject, name='superadmin-editobject'),
    path('object/<int:id>/delete/', superadmin_deleteobject, name='superadmin-deleteobject'),
]