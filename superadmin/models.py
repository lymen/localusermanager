from django.db import models
from django.urls import reverse

# Create your models here.
class SuperAdmin(models.Model):
	username	= models.CharField(max_length=120, unique=True)
	password	= models.CharField(max_length=120)

class UserGroup(models.Model):
	groupname	= models.CharField(max_length=120, unique=True)

	def __str__(self):
		return u'{0}'.format(self.groupname)

class User(models.Model):
	username	= models.CharField(max_length=120, unique=True)
	password	= models.CharField(max_length=120)
	group		= models.ForeignKey(UserGroup, on_delete=models.CASCADE)

class Account(models.Model):
	username	= models.CharField(max_length=120, unique=True)
	password	= models.CharField(max_length=120)
	group		= models.ForeignKey(UserGroup, on_delete=models.CASCADE)

	def __str__(self):
		return u'{0}'.format(self.username)

class AccountChangeLog(models.Model):
	username	= models.ForeignKey(Account, on_delete=models.CASCADE)
	password	= models.CharField(max_length=120)
	modified	= models.DateTimeField(auto_now_add=True)
