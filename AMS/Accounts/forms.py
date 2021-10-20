# accounts.forms.py
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    employee_id=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['employee_id'].widget.attrs['class'] ='input'
        self.fields['employee_id'].widget.attrs['placeholder'] ='Employee Id'
        self.fields['password'].widget.attrs['class'] ='input'
        self.fields['password'].widget.attrs['placeholder'] ='Password'
    
    def clean_employee_id(self):
        emp=self.cleaned_data.get('employee_id',False)
        if(emp and emp.isalnum() and emp.startswith("EMP")):
            try:
                User.objects.get(Employee_Id=emp)
            except:
                raise forms.ValidationError("Employee Id is Not Available.!")
        else:
            raise forms.ValidationError("Please Enter Valid Employee Id .!")
        return emp
    
    def clean_password(self):
        password=self.cleaned_data.get('password',False)
        if(password and len(password)>1):
            pass
        else:
            raise forms.ValidationError("Please Enter Password Correctly .!")
        return password

    def clean(self):
        cleaned_data=super().clean()
        employee_id=cleaned_data.get('employee_id',None)
        password_=cleaned_data.get('password',None)
        if employee_id and password_:
            try:
                user=User.objects.get(Employee_Id=employee_id)
            except:
                raise forms.ValidationError("Please Provide Valid Details !")
            if(not user.active):
                raise forms.ValidationError("Your Employee ID is Not Active !!.Get Approval from Manager !")
            
        else:
            raise forms.ValidationError("Please Enter Valid Details .!")




    

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email','full_name','phonenumber')
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs['placeholder'] = 'Full Name'
        self.fields['full_name'].widget.attrs['id'] = 'full_name'
        self.fields['full_name'].widget.attrs['class'] = 'input'
        self.fields['phonenumber'].widget.attrs['placeholder'] = 'Phone Number'
        self.fields['phonenumber'].widget.attrs['id'] = 'phonenumber'
        self.fields['phonenumber'].widget.attrs['class'] = 'input'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['email'].widget.attrs['id'] = 'email'
        self.fields['email'].widget.attrs['class'] = 'input'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].widget.attrs['id'] = 'password1'
        self.fields['password1'].widget.attrs['class'] = 'input'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].widget.attrs['id'] = 'password2'
        self.fields['password2'].widget.attrs['class'] = 'input'
    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email is already taken .!")
        return email
    
    def clean_phonenumber(self):
        phonenumber = self.cleaned_data.get('phonenumber')
        if(len(str(phonenumber)) != 10):
            raise forms.ValidationError("Enter Valid Phonenumber .!") 
        qs = User.objects.filter(phonenumber=phonenumber)
        if qs.exists():
            raise forms.ValidationError("Phonenumber is Already taken .!")
        return phonenumber

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if not password1 or len(str(password1))<5:
            raise forms.ValidationError("Enter Valid Password.!")
        return password1

    def clean_password2(self):
        password2 = self.cleaned_data.get("password2")
        if not password2 or len(str(password2))<5:
            raise forms.ValidationError("Enter Valid Password.!")
        return password2
    
    
    def clean(self):
        cleaned_data=super().clean()
        password2 = self.cleaned_data.get("password2")
        password1 = self.cleaned_data.get("password1")
        if(password1 and password2):
            if(password1!=password2):
                raise forms.ValidationError("Password Not Matched .!")
        else:
            raise forms.ValidationError("Enter Passwrods .!")


class UserAdminCreationForm(forms.ModelForm):

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email','full_name','phonenumber','admin')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.active=True
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email','full_name','phonenumber', 'password', 'active', 'admin')

    def clean_password(self):
        return self.initial["password"]