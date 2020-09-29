from django.urls import path
from .views import (
	account_register,
	)

app_name = 'account'
urlpatterns = [
    # path('product/', product_detail_view),
    path('', account_register, name='account-register'),
]