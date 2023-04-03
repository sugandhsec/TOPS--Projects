from django.db import models
from random import choices
from secrets import choice
from turtle import position
from django.db import models
from django.utils import timezone


user_type = (
	("Vistor", "Visitor"),
	("user", "user"),
)

# Create your models here.
class User(models.Model):
	fname=models.CharField(max_length=100)
	lname=models.CharField(max_length=100)
	email=models.EmailField()
	address=models.TextField()
	city=models.CharField(max_length=100)
	zipcode=models.PositiveIntegerField()
	mobile=models.PositiveIntegerField()
	password=models.CharField(max_length=100)
	profile_pic=models.ImageField(upload_to="profile_pic/")
	usertype=models.CharField(max_length=100,choices=user_type)
	

	def __str__(self):
		return self.fname+" "+self.lname

class Signup(models.Model):
	fname=models.CharField(max_length=100)
	lname=models.CharField(max_length=100)
	email=models.EmailField(default='')
	emp_code=models.PositiveIntegerField()
	reason=models.TextField()
	amount=models.TextField()
	date=models.DateTimeField(default=timezone.now)
	made_on = models.DateTimeField(default=timezone.now)
	current_status = models.CharField(max_length=10, default="Entry")
	

	def __str__(self):
		return self.fname+" "+self.lname

class petty_amount(models.Model):
	amount_present=models.IntegerField(default=0)

	def __str__(self):
		return str(self.amount_present)
	
class log(models.Model):
	fname=models.CharField(max_length=100)
	lname=models.CharField(max_length=100)
	email=models.EmailField(default='')
	emp_code=models.PositiveIntegerField()
	reason=models.TextField()
	amount=models.TextField()
	type=models.TextField(default='Debit')
	petty_amount=models.TextField(default='0')
	current_status = models.CharField(max_length=10, default="Entry")
	date=models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.fname+" "+self.lname