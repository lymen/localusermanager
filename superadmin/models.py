from django.db import models
from django.urls import reverse

# Create your models here.
class SuperAdmin(models.Model):
	username	= models.CharField(max_length=120, unique=True)
	password	= models.CharField(max_length=120)

class UserGroup(models.Model):
	groupname	= models.CharField(max_length=120, unique=True)

	def get_absolute_url(self):
		# return f"/product/{self.id}/"
		return reverse("superadmin:superadmin-editgroup", kwargs={"id": self.id})

class User(models.Model):
	username	= models.CharField(max_length=120, unique=True)
	password	= models.CharField(max_length=120)
	group		= models.ForeignKey(UserGroup, on_delete=models.CASCADE)

class Object(models.Model):
	username	= models.CharField(max_length=120, unique=True)
	password	= models.CharField(max_length=120)
	group		= models.ForeignKey(UserGroup, on_delete=models.CASCADE)

class ObjChangeLog(models.Model):
	username	= models.ForeignKey(Object, on_delete=models.CASCADE)
	password	= models.CharField(max_length=120)
	datachanged	= models.DateTimeField()