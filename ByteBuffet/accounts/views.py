from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required, user_passes_test
import traceback
from django.core.exceptions import PermissionDenied

from .utils import detectUser

from django.http import HttpResponse
from .forms import UserForm
from .models import MyUser ,UserProfile
from vendor.forms import VendorForm
from django.contrib import messages #import messages


# Create your views here.
def registerUser(request):
    if request.method == "POST":
        form = UserForm(request.POST)

        if form.is_valid():

            # password=form.cleaned_data['password']
            # user=form.save(commit=False) # form is not yet submited , yet to submit

            # user.set_password(password)

            # user.role=MyUser.CUSTOMER
            # user.save()

            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']

            user=MyUser.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role=MyUser.CUSTOMER
            user.save()
            
            messages.success(request, "Your Accout has been succesfull regsiterd🍻." )
            
        else:
            print("error")
            messages.error(request, "Error. Form not sumitted😣.")


    else:
        form = UserForm()  

    context = {
        'form': form,
    }
    return render(request, 'accounts/registrationUser.html', context)



def registerVendor(request):
    if request.user.is_authenticated:
            messages.warning(request, 'You are already logged in.')
            return redirect('dashboard')
   
    elif request.method == 'POST':

        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)

        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # vendor_license=
            user = MyUser.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = MyUser.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            # vendor_name = v_form.cleaned_data['vendor_name']
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()

         
            messages.success(request, 'Your account has been registered sucessfully! Please wait for the approval.')
            return redirect('registerVendor')
        else:
            print('invalid form')
            print(form.errors)
            print(v_form.errors)
    else:
        form = UserForm()
        v_form = VendorForm()

    context = {
        'form': form,
        'v_form': v_form,
    }

    return render(request, 'accounts/registerVendor.html', context)

from django.contrib import auth
from django.contrib import messages

def login(request):
    try:
        if request.user.is_authenticated:
            messages.warning(request, 'You are already logged in.')
            return redirect('myAccount')
        
        elif request.method == 'POST':
            email = request.POST.get("email").strip()
            password = request.POST.get("password").strip()

            user = authenticate(email=email, password=password)
            if user is not None:
                auth_login(request, user)
                print("Email:", email)
                print("Password:", password)
                messages.success(request, 'Login successful.')
                return redirect('myAccount')
            else:
                print("Email:", email)
                print("Password:", password)
                messages.error(request, 'Invalid email or password. Please try again.')
        else:
            return render(request, 'accounts/login.html')  # Add this line for GET requests
    except Exception as e:
        traceback.print_exc()
        messages.error(request, 'An error occurred during login. Please try again.')
    return render(request, 'accounts/login.html')
 
@login_required(login_url='login')
def user_logout(request):
    logout(request)
    messages.success(request, 'Logout successful.')
    return redirect('home')

@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)



# Restrict the vendor from accessing the customer page
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


# Restrict the customer from accessing the vendor page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied



@login_required(login_url='login')  
@user_passes_test(check_role_customer)
def customerdashboard(request):
    return render(request, 'accounts/customerdashboard.html')

@login_required(login_url='login') 
@user_passes_test(check_role_vendor)

def vendordashboard(request):
    return render(request, 'accounts/vendordashboard.html')