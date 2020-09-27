from django.contrib import admin

# Register your models here.
from .models import (
	SuperAdmin,
	UserGroup,
	User,
	Object,
	ObjChangeLog
)

admin.site.register(SuperAdmin)
admin.site.register(UserGroup)
admin.site.register(User)
admin.site.register(Object)
admin.site.register(ObjChangeLog)
