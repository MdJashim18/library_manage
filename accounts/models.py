# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
# from django.conf import settings

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('librarian', 'Librarian'),
        ('admin', 'admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')


class Student(models.Model):
    user = models.OneToOneField("accounts.CustomUser", on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    father_name = models.CharField(max_length=30)
    mother_name = models.CharField(max_length=30)
    email = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    registration = models.IntegerField(unique=True)
    religion = models.CharField(max_length=20)
    birthdate = models.DateField()
    marital_status = models.CharField(max_length=20)
    nationality = models.CharField(max_length=50)
    image = models.ImageField(upload_to="students/", blank=True, null=True)


class Teacher(models.Model):
    user = models.OneToOneField("accounts.CustomUser", on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    father_name = models.CharField(max_length=30)
    mother_name = models.CharField(max_length=30)
    email = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    registration = models.IntegerField(unique=True)
    religion = models.CharField(max_length=20)
    birthdate = models.DateField()
    marital_status = models.CharField(max_length=20)
    nationality = models.CharField(max_length=50)
    image = models.ImageField(upload_to="teachers/", blank=True, null=True)



class Librarian(models.Model):
    user = models.OneToOneField("accounts.CustomUser", on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    father_name = models.CharField(max_length=30)
    mother_name = models.CharField(max_length=30)
    email = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    registration = models.IntegerField(unique=True)
    religion = models.CharField(max_length=20)
    birthdate = models.DateField()
    marital_status = models.CharField(max_length=20)
    nationality = models.CharField(max_length=50)
    image = models.ImageField(upload_to="librarians/", blank=True, null=True)

