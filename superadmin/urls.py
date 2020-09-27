from django.urls import path
from .views import (
	superadmin_login,
	superadmin_user,
	superadmin_group,
	superadmin_object,
	superadmin_editgroup,
	superadmin_deletegroup,
	# validate_username
	)

app_name = 'superadmin'
urlpatterns = [
    # path('product/', product_detail_view),
    path('', superadmin_login, name='superadmin-login'),
    path('user', superadmin_user, name='superadmin-user'),
    path('group', superadmin_group, name='superadmin-group'),
    # path('group/<int:id>/', superadmin_editgroup2, name='superadmin-editgroup'),
    path('group/<int:id>/edit/', superadmin_editgroup, name='superadmin-editgroup'),
    path('group/<int:id>/delete/', superadmin_deletegroup, name='superadmin-deletegroup'),
    # path('validate/<int:id>/', validate_username, name='validate'),
    path('object', superadmin_object, name='superadmin-object'),
]