from django.contrib import admin

# Register your models here.
from .models import (
	SuperAdmin,
	UserGroup,
	User,
	Account,
	AccountChangeLog
)

admin.site.register(SuperAdmin)
admin.site.register(UserGroup)
admin.site.register(User)
admin.site.register(Account)
admin.site.register(AccountChangeLog)
