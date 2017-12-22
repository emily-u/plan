from __future__ import unicode_literals
import bcrypt
from datetime import datetime
from django.db import models
import re
name_regex = re.compile(r'^[A-Z][a-zA-Z]{3,}(?: [A-Z][a-zA-Z]*){0,2}$')

class UserManager(models.Manager):
    def regis_validator(self, post):
        name = post['name']
        username = post['username']
        password = post['password']
        cpassword = post['cpassword']


        errors=[]

        if len(name)<3 or len(username)<3 or len(password)<1 or len(cpassword)<1:
            errors.append("all fields are required, and at least 3 characters for the name and username")
        else:
            if not name.isalpha():
                errors.append("incorrect name format")
            else:
                if len(User.objects.filter(username=username)) > 0 :
                    errors.append('username is already used')

            if len(password) < 8 :
                errors.append('password: at least 8 characters')
            elif password != cpassword:
                errors.append('password is not match with comfirm password, please try again')
            
        if not errors:
            hashed = bcrypt.hashpw((password.encode()), bcrypt.gensalt(5))

            new_user = self.create(
                name=name,
                username=username,
                password=hashed
            )
            return new_user                

        return errors

    def login_validator(self, post):
        username = post['username']
        password = post['password']

        try:
            user = User.objects.get(username=username)
            if bcrypt.checkpw(password.encode(), user.password.encode()):
                return user
        except:
            pass

        return False

    def plan_validator(self, post):
        destination = post['destination']
        description = post['description']
        startdate = post['startdate']
        enddate = post['enddate']
        # errors=[]
        errors = {}
        date_regex = re.compile(r'^(((0?[1-9]|1[012])/(0?[1-9]|1\d|2[0-8])|(0?[13456789]|1[012])/(29|30)|(0?[13578]|1[02])/31)/(19|[2-9]\d)\d{2}|0?2/29/((19|[2-9]\d)(0[48]|[2468][048]|[13579][26])|(([2468][048]|[3579][26])00)))$') 
        if len(destination)<1 or len(description)<1 or len(startdate)<1 or len(enddate)<1:
            errors.append("all fields are required")
        else:
            startdate = datetime.strptime(startdate, '%Y-%m-%d')
            enddate = datetime.strptime(enddate, '%Y-%m-%d')
            if startdate < datetime.now():
                errors['startdate'] = "Start date should be future date."
            
            if startdate > enddate:
                errors['date'] = "Start date should be before end date."
        
        return errors
          
    
class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()


class Plan(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    startdate = models.DateField(null=True, blank=True)
    enddate = models.DateField(null=True, blank=True)
    creator = models.ForeignKey(User,related_name='createplan')
    follower = models.ManyToManyField(User, related_name="joinplan")

    objects = UserManager()