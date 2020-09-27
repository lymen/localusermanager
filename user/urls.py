from django.urls import path
from .views import (
	user_login,
	user_home,
	)

app_name = 'user'
urlpatterns = [
    # path('product/', product_detail_view),
    path('', user_login, name='user-login'),
    path('home', user_home, name='user-home'),
]