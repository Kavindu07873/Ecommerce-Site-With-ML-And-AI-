from django.db import models
from django.contrib.auth.models import AbstractBaseUser ,BaseUserManager
# Create your models here.

# create super admin
class MyAccountManager(BaseUserManager):
    # creating a normal user
    def create_user(self,first_name,last_name,username,email,password=None):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have an username')
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            # phone_number= phone_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # creating a super user

    def create_superuser(self,first_name,last_name,email,username,password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password=password,
            first_name = first_name,
            last_name = last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using = self._db)
        return user




# acount creation
class Account(AbstractBaseUser):
    first_name   = models.CharField(max_length=50)
    last_name    = models.CharField(max_length=50)
    username     = models.CharField(max_length=50 ,unique=True)
    email        = models.EmailField(max_length=100 , unique=True) 
    phone_number = models.CharField(max_length=50)

    # required Custom user model
    date_joined     =models.DateTimeField(auto_now_add=True)
    last_login      =models.DateTimeField(auto_now_add=True)
    is_admin        =models.BooleanField(default=False)
    is_staff        =models.BooleanField(default=False)
    is_active       =models.BooleanField(default=False)
    is_superadmin   =models.BooleanField(default=False)
    
    # username field eka email karanna ona
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name' , 'last_name']

    # api super user eka use karanawa kiyanna ona
    objects =MyAccountManager() 

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    # return karanne email eka acount eke object eka widiyata template ekata
    def __str__(self):
        return self.email
    
    # custom user model ekak hadanakota api aniwaren mention karanna ona dewal thiyenawa
    # addminta permition thiyenawa  Account manage karanna
    def has_perm(self , perm ,obj=None):
        return self.is_admin
    
    def has_module_perms(self,add_label):
        return True
    


class UserProfile(models.Model):
    user = models.OneToOneField(Account , on_delete=models.CASCADE)
    address_line_1 = models.CharField(blank=True ,max_length=100)
    address_line_2 = models.CharField(blank=True ,max_length=100)
    profile_picture = models.ImageField(blank=True ,upload_to='userprofile')
    city = models.CharField(blank=True , max_length=20 )
    state = models.CharField(blank=True , max_length=20 )
    country = models.CharField(blank=True , max_length=20)

    def __str__(self):
        return self.user.first_name
    
    def full_address(self):
        return f'{self.address_line_1}{self.address_line_2}'
    
    
    