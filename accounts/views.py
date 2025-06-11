
import pytz
import secrets
import random

from django.urls import reverse
from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext as _
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password 


from utils import send_otp_code
from .models import MyUser, OtpCode
from .forms import ForgotPasswordForm, ResetPasswordForm, UserRegisterForm, VerifyCodeForm 


class UserRegisterView(View):
    form_class = UserRegisterForm
    def get(self, request):
        form= self.form_class
        return render(request, 'accounts/user_register.html', {'form':form})
    
    def post(self, request):
        form =self.form_class(request.POST)
        if form.is_valid():
            otp = OtpCode.objects.filter(phone_number = form.cleaned_data['phone'])
            if otp.exists():
                messages.error(request, _('we send your code already'))
                return redirect('accounts:verify_code')
            random_code = random.randint(1000, 9999)
            send_otp_code(form.cleaned_data['phone'], random_code)
            OtpCode.objects.create(phone_number=form.cleaned_data['phone'], code=random_code)
            request.session['user_registration_info']={
                'phone_number':form.cleaned_data['phone'],
                'full_name':form.cleaned_data['full_name'],
                'password':form.cleaned_data['password2'],
            }
            messages.success(request, _('we sent you a code'))
            return redirect('accounts:verify_code')
        return render(request, 'accounts/user_register.html', {'form':form})


class UserRegisterCodeView(View):
    form_class = VerifyCodeForm
    def get(self, request):
        form = self.form_class()
        user_session = request.session.get('user_registration_info')
        if not user_session:
            messages.error(request, _('Registration information not found.'))
            return redirect('accounts:user_register')  
        return render(request, 'accounts/verify_code.html', context={'form': form})

    def post(self, request):
        user_session = request.session.get('user_registration_info')
        if not user_session:
            messages.error(request, _('Registration information not found.'))
            return redirect('accounts:user_register')  
        
        code_instance = OtpCode.objects.filter(phone_number=user_session['phone_number']).first()

        if not code_instance:
            messages.error(request, _('No code was found for this phone number.'))
            return redirect('accounts:user_register')
        
        form = self.form_class(request.POST)
        
        if form.is_valid():
            cd = form.cleaned_data
            now = datetime.now(tz=pytz.timezone('Asia/Tehran'))
            expired_time = code_instance.date_time_created + timedelta(minutes=2) 
            
            if now > expired_time:
                code_instance.delete()
                messages.error(request, _('The OTP code has expired.'))
                return redirect('accounts:user_register')  
            
            if cd['code'] == code_instance.code:
                user = MyUser.objects.create_user(user_session['phone_number'], user_session['full_name'], user_session['password'])
                code_instance.delete() 
                messages.success(request, _('You have successfully registered.'))
                login(request, user)  
                return redirect('store:product_list') 
            else:
                messages.error(request, _('This code is incorrect.'))
                return redirect('accounts:verify_code')  
        
        return redirect('store:product_list') 


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next')
                if next_url:
                    messages.success(request, _('You have successfully logged in.'))
                    return  redirect(next_url)
                else:
                    messages.success(request, _('You have successfully logged in.'))
                    return redirect('store:product_list')
            else:
                messages.warning(request, _("this phone number does not exist please already registered"))
                return redirect('store:product_list') 
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', context={'form': form})



def logout_view(request):
    if request.method =='POST':
        logout(request)
        messages.error(request, _('you successfully logout'))
        return redirect('store:product_list')



@login_required
def password_change_view(request):
    if request.method =='POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            messages.success(request, _('your password successfully changed'))
            return redirect('store:product_list')
        return redirect('accounts:change_password')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'accounts/password_change.html',{'form':form})


def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']

            User = get_user_model() 
            try:
                user = User.objects.get(phone_number=phone_number)
            except User.DoesNotExist:
                messages.error(request, "این شماره تلفن در سیستم ثبت نشده است.")
                return render(request, 'forgot_password.html', {'form': form})

            random_code = random.randint(1000, 9999)
            send_otp_code(phone_number, random_code)
            OtpCode.objects.create(phone_number=phone_number, code=random_code)

            request.session['reset_phone'] = str(phone_number) 
            request.session['reset_code'] = random_code 
            messages.success(request, "کد تایید به شماره تلفن شما ارسال شد.")
            return redirect(reverse('accounts:reset_password')) 

    else:
        form = ForgotPasswordForm()
    return render(request, 'accounts/forgot_password.html', {'form': form})



def reset_password(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            new_password = form.cleaned_data['new_password1']

            reset_phone = request.session.get('reset_phone') 
            reset_code = request.session.get('reset_code') 

            if not reset_phone or not reset_code:
                messages.error(request, "درخواست نامعتبر است. لطفا دوباره تلاش کنید.")
                return redirect(reverse('accounts:forgot_password'))
            if str(code) == str(reset_code):
                User = get_user_model()
                try:
                    user = User.objects.get(phone_number=reset_phone)
                except User.DoesNotExist:
                    messages.error(request, "کاربر یافت نشد.")
                    return render(request, 'reset_password.html', {'form': form}) 

                user.password = make_password(new_password) 
                user.save()

        
                del request.session['reset_phone']
                del request.session['reset_code']
                update_session_auth_hash(request, user)
                messages.success(request, "رمز عبور شما با موفقیت تغییر یافت.")
                return redirect('accounts:login')  
            else:
                messages.error(request, "کد تایید صحیح نیست.")

    else:
        form = ResetPasswordForm()
    return render(request, 'accounts/reset_password.html', {'form': form})
