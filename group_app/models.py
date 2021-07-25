from django.db import models
import re
from django.db.models.base import Model

# Validations

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def registration_validator(self, postData):
        
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "The first name entered is incorrect, you must enter more than 3 characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "The last name entered is incorrect, you must enter more than 3 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "The email entered is incorrect"
        registered_users_email = User.objects.filter(email = postData['email'])
        if len(registered_users_email)>= 1:
            errors['duplicate'] = "Email already exist"
        if len(postData['password']) < 8:
            errors['password'] = "The password must be greater than 8 characters"
        return errors


class OrgManager(models.Manager):
    def org_validator(self, postData):

        errors = {}
        if len(postData['name']) < 6:
            errors['name'] = "Invalid Organization Name. should be more than 5 characters"
        if len(postData['description']) < 11:
            errors['description'] = "Invalid description. should be more than 10 characters"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Org(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(User, related_name="orgs")
    objects = OrgManager()
