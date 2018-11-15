from __future__ import unicode_literals
from django.db import models
import re, bcrypt

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        if 'first_name' not in postData:
            errors['no_first_name'] = "Did not enter a first name"
        if len(postData['first_name']) < 2:
            errors['first_name'] = "Course name must have at least 2 characters"
        if 'last_name' not in postData:
            errors['no_last_name'] = "Did not enter a last name"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must have at least 2 characters"
        if 'email' not in postData:
            errors['no_email'] = "Did not enter an email"
        email = postData['email']
        if not re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email):
            errors['valid_email'] = "Not a valid email"
        if len(postData['password']) < 8:
            errors['password'] = "Password must have at least 8 characters"
        if postData['password'] != postData['confpw']:
            errors['no_match'] = "The passwords do not match"
        return errors
    def login_validator(self, postData):
        errors ={}
        if 'login_email' not in postData:
            errors['no_email'] = "Did not enter an email"
        if 'login_password' not in postData:
            errors['no_password'] = "Did not enter a password"
        if not User.objects.filter(email = postData['login_email']).exists():
            errors['no_email'] = "That email is not registered"
        elif not bcrypt.checkpw(postData['login_password'].encode(), User.objects.get(email = postData['login_email']).password.encode()):
            errors['wrong_password'] = "Wrong password. Please try again"
        return errors
    def edit_validator(self, postData):
        errors ={}
        if 'edit_first_name' not in postData:
            errors['no_first_name'] = "Did not enter a first name"
        if len(postData['edit_first_name']) < 2:
            errors['first_name'] = "First name must have at least 2 characters"
        if 'edit_last_name' not in postData:
            errors['no_last_name'] = "Did not enter a last name"
        if len(postData['edit_last_name']) < 2:
            errors['last_name'] = "Last name must have at least 2 characters"
        if 'edit_email' not in postData:
            errors['no_email'] = "Did not enter an email"
        email = postData['edit_email']
        if not re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email):
            errors['valid_email'] = "Not a valid email"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class QuoteManager(models.Manager):
    def quote_validator(self, postData):
        errors = {}
        if 'author' not in postData:
            errors['no_author'] = "Did not input an author name!"
        if len(postData['author']) < 3:
            errors['author'] = "Author name must contain more than 3 characters!"
        if 'quote' not in postData:
            errors['no_quote'] = "Did not input a quote!"
        if len(postData['quote']) < 10:
            errors['quote'] = "Quote must be more than 10 characters!"
        return errors


class Quote(models.Model):
    author = models.CharField(max_length=255)
    quote = models.TextField()
    posted_by = models.ForeignKey(User, related_name="quotes")
    likes = models.ManyToManyField(User, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()

# Create your models here.
