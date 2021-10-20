from django.contrib.auth.models import BaseUserManager
from django.utils.translation import ugettext_lazy as _

class MyUserManager(BaseUserManager):
	def create_user(self,full_name,phonenumber,email,password,admin=False,active=False):
		if not full_name:
			raise ValueError(_("Please Enter Full Name !"))
		if not phonenumber:
			raise ValueError(_("Please Enter Phone Number !"))
		if not email:
			raise ValueError(_("Please Enter Email !"))
		if not password:
			raise ValueError(_("Please Enter Password !"))

		user=self.model(email=self.normalize_email(email),
						full_name=full_name,
						phonenumber=phonenumber,
						admin=admin,
						active=active
							)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self,full_name,phonenumber,email,password,admin=True,active=True,Employee_Id=None):
		user=self.create_user(full_name,phonenumber,email,password,admin,active)
		user.save(using=self._db)
		return user