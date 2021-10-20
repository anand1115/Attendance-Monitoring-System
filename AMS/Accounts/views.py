from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib.auth import authenticate,login,logout
from .models import User
from .forms import *

# Create your views here.


class LoginView(View):
    def get(self,request):
        return render(request,'Accounts/login.html',{"form":LoginForm()})
    
    def post(self,request):
        context={}
        error=False
        context['form']=LoginForm()
        try:
            form=LoginForm(request.POST)
            if(form.is_valid()):
                empid=form.cleaned_data['employee_id']
                password=form.cleaned_data['password']
                log=authenticate(request,Employee_Id=empid,password=password)
                if(log is not None):
                    login(request,log,backend='django.contrib.auth.backends.ModelBackend')
                    return redirect("Accounts:login")
                else:
                    error="Enter Valid Details.!"
            else:
                try:
                    error=list(form.errors.values())[0][0]
                except:
                    error="Try Again with Valid Details"
            context['form']=form
        except Exception as err:
            error=err
        context['error']=error
        return render(request,'Accounts/login.html',context) 


class SignupView(View):

    def get(self,request):
    	return render(request,'Accounts/signup.html',{"form":RegisterForm()})
    
    def post(self,request):
        context={}
        error=False
        try:
            form=RegisterForm(request.POST)
            if(form.is_valid()):
                full_name=form.cleaned_data.get('full_name')
                phonenumber=form.cleaned_data.get('phonenumber')
                email=form.cleaned_data.get('email')
                password1=form.cleaned_data.get('password1')
                password2=form.cleaned_data.get('password2')
                if(password1==password2):
                    try:
                        User.objects.create_user(full_name=full_name,phonenumber=phonenumber,email=email,password=password2)
                        return redirect("Accounts:login")
                    except:
                        error="Try again with Valid details"
                else:
                    error="Passwords Not Matched"
            else:
                error=list(form.errors.values())[0][0]
            context['form']=form
        except Exception as err:
            error=err
        context['error']=error
        return render(request,'Accounts/signup.html',context)
