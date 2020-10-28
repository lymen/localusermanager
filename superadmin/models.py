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
	group		= models.ManyToManyField(UserGroup, blank=False)

	def get_group_values(self):
		ret = ''
		print(self.group.all())

		for group in self.group.all():
			ret = ret + group.groupname + ', '

		return ret[:-2]

class Account(models.Model):
	username	= models.CharField(max_length=120, unique=True)
	password	= models.CharField(max_length=120)
	group		= models.ManyToManyField(UserGroup)

	def __str__(self):
		return u'{0}'.format(self.username)

	def get_group_values(self):
		ret = ''
		print(self.group.all())

		for group in self.group.all():
			ret = ret + group.groupname + ', '

		return ret[:-2]

class AccountChangeLog(models.Model):
	username	= models.ForeignKey(Account, on_delete=models.CASCADE)
	password	= models.CharField(max_length=120)
	modified	= models.DateTimeField(auto_now_add=True)
