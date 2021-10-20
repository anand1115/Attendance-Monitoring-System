from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .managers import MyUserManager

# Create your models here.

class User(AbstractBaseUser,PermissionsMixin):
    Employee_Id=models.CharField(max_length=250,editable=False,unique=True)
    full_name=models.CharField(max_length=250)
    phonenumber=models.CharField(max_length=250,unique=True)
    email=models.EmailField(unique=True,max_length=250)
    active=models.BooleanField(default=False)
    admin=models.BooleanField(default=False)

    USERNAME_FIELD="Employee_Id"
    REQUIRED_FIELDS=['full_name','email','phonenumber']
    objects=MyUserManager()

    def __str__(self):
        return str(self.Employee_Id)

    def save(self,*args,**kwargs):
        if not self.Employee_Id:
            total=User.objects.count()
            self.Employee_Id="{}{:02d}".format("EMP",int(total)+1 if total else 1)
        super().save(*args,**kwargs)
    
    def is_active(self):
        return self.active
    
    def is_admin(self):
        return self.admin

    def is_staff(self):
        return self.admin
    
    def has_perm(self,perm,obj=None):
        return True
    
    def has_perms(self,perm,obj=None):
        return True
    
    def has_module_perms(self,app_label):
        return True

