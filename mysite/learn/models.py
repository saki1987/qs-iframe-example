from django.db import models

# Create your models here.


class TestedDomain(models.Model):
	domain = models.CharField(max_length = 256)
	userid = models.IntegerField()

	def __unicode__(self):
		return self.domain

class User(models.Model):
	username = models.CharField(max_length = 64)
	password = models.CharField(max_length = 64)
	email	 = models.EmailField(max_length = 128)
	phone	 = models.IntegerField()
	
	def __unicode__(self):
		return self.username
