from django.contrib import messages
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from App_Accounts.forms import *
from App_Accounts.models import user_Apportionment, Profile,HLogin

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import response
from twilio.rest import Client
import datetime
from django.http import HttpResponse
from django.views.generic import View

from App_Accounts.utils import render_to_pdf #created in step 4  



def Signupview(request):
    if request.user.is_authenticated:
        return redirect('App_Blood:index')
    else:
        try:
            if request.method == "POST":
                form = SignUpForm(request.POST or None)
                if form.is_valid():
                    user = form.save()
                    user.refresh_from_db()
                    user.profile.type = form.cleaned_data.get('type')
                    user.profile.phone = form.cleaned_data.get('phone')
                    user.save()
                    messages.success(request, "Signup Done,Please Login to Complete your Profile",
                                     extra_tags="signup_complete")
                    return redirect(request.POST['next'])
            else:
                form = SignUpForm()
        except:
            return redirect('App_Accounts:signup')

        context = {
            'form': form,
        }
        return render(request, 'App_Accounts/signuppage.html', context)


def Loginview(request):
    if request.user.is_authenticated:
        return redirect('App_Blood:index')
    else:
        if request.method == "POST":
            user_name = request.POST.get('username')
            password = request.POST.get('password')
            next = request.GET.get("next", '')
            user = authenticate(request, username=user_name, password=password)
            if user is not None:
                login(request, user)
                if next != "":
                    return redirect(next)
                return redirect('App_Accounts:dashboard')
            else:
                messages.info(request, "Enter correct username and password", extra_tags="login_error")
                return redirect('App_Accounts:login')
        else:
            return render(request, 'App_Accounts/login.html')
def HRLoginview(request):
    return render(request, 'App_Accounts/hlogin.html')

def hLoginview(request):
    if request.method == "POST":
        user_name = request.POST.get('username')
        password = request.POST.get('password')
        getHospital = HLogin.objects.filter(username=user_name)
        if getHospital:
            Huser_name = getHospital[0].username
            Hpassword = getHospital[0].password
            if(user_name == Huser_name and password == Hpassword):
                return redirect('/doner')
            else:
                messages.info(request, "Enter correct username and password", extra_tags="login_error")
                return redirect('App_Accounts:hlogin')
        else:
            messages.info(request, "Enter correct username and password", extra_tags="login_error")
            return redirect('App_Accounts:hlogin')
    else:
        return render(request, 'App_Accounts/hlogin.html')


@login_required(login_url='App_Accounts:login')
def Logoutview(request):
    logout(request)
    return redirect('App_Accounts:login')


@login_required(login_url='App_Accounts:login')
def Dashboard(request):
    return render(request, 'App_User/index.html')


@login_required(login_url='App_Accounts:login')
def Profileupdate(request):
    try:
        if request.method=="POST":
            form=ProfileUpdateForm(request.POST or None,request.FILES,instance=request.user.profile)
            form_2=UserUpdateForm(request.POST or None,instance=request.user)
            if form.is_valid():
                form.save()
                form_2.save()
                messages.success(request,"Profile Update successfully",extra_tags="profile_update")
                return redirect(request.POST['next'])
        else:
            form=ProfileUpdateForm(instance=request.user.profile)
            form_2 = UserUpdateForm(instance=request.user)
    except:
        return redirect('App_Accounts:dashboard')

    context={
        'form':form,
        'form_2':form_2,
    }
    return render(request, 'App_User/updateprofile.html',context)


@login_required(login_url="App_Accounts:login")
def PasswordChange(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!', extra_tags="pass_change")
            return redirect('App_Accounts:passwordchange')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'App_User/change_password.html', {
        'form': form
    })


@login_required(login_url="App_Accounts:login")
def save_Apportionment(request):
    user = request.user
    TodayDayte = datetime.date.today()
    objxx = Profile.objects.get(user=user)
    objyy = objxx.lastdonate
    objzz = datetime.date(objyy.year, objyy.month, objyy.day)
    aaac = str(TodayDayte-objzz)
    if(aaac == "0:00:00"):
        messages.error(request, "your are Currently Not Elegible for Donating the Blood. You Elegible after 90 days !!")
        return redirect('/accounts/dashboard')
    else:
        bbbc = aaac.split(", ")
        cccc = bbbc[0].split(" ")
        varxxxy = 90-int(cccc[0])
        if(int(cccc[0])>=90):
            name = request.POST['name']
            gender = request.POST['gender']
            date_of_birth = request.POST['date_of_birth']
            mobile_no = request.POST['mobile_no']
            address = request.POST['address']
            apportionment_date = request.POST['apportionment_date']
            state = request.POST['state']
            city = request.POST['city']
            blood_bank_name = request.POST['blood_bank_name']
            blood_group = request.POST['blood_group']
            # g_id = request.POST['g_id']
            SaveApportionment = user_Apportionment(user=user, name=name, gender=gender, date_of_birth=date_of_birth, mobile_no= mobile_no, address=address, apportionment_date=apportionment_date,state=state, city=city, blood_bank_name=blood_bank_name, blood_group=blood_group)
            SaveApportionment.save()
            obj = Profile.objects.get(user=user)
            obj.points += 15
            obj.lastdonate = apportionment_date
            obj.latestHospital = blood_bank_name
            obj.latestCity = city
            obj.latestName =name
            obj.save()
            messages.success(request, 'your Apportionment is sucessfully Booked!!')
            return redirect('/accounts/dashboard')
        else:
            messages.error(request, 'your are Currently Not Elegible for Donating the Blood. You Elegible after '+str(varxxxy)+" days !!")
            return redirect('/accounts/dashboard')


@login_required(login_url="App_Accounts:login")
def reward(request):
    user = request.user
    fetchProfile = Profile.objects.filter(user = user)
    
    return render(request, 'App_User/store.html', {
        'fetchProfile': fetchProfile
    })

@login_required(login_url="App_Accounts:login")
def Certificate(request):
    user = request.user
    fechPData = Profile.objects.filter(user = user)
    dataxx = {'fechPData':fechPData}
    pdf = render_to_pdf('certificate.html', dataxx)
    return HttpResponse(pdf, content_type='application/pdf')

@login_required(login_url="App_Accounts:login")
@api_view(['POST'])
def updatePoints(request):
    if request.method == 'POST':
        userx = request.user
        contactX = request.data
        print(contactX)
        contact = contactX["points"]
        print(contact)
        userxx = Profile.objects.filter(user = userx)
        points = [itemx.points for itemx in userxx]
        status = points[0]-contact
        print(status)
        Profile.objects.filter(user = userx).update(points = status)
        userMessage = "Thank you for placing an order in the BloodLab Rewards Zone. Your order is being processed! "
        account_sid = 'ACc17206d59f27e0c0be30ceb0d08cc5d7'
        auth_token = '51c140fe5515c1cd0192697cf3916193'
        client = Client(account_sid, auth_token)

        client.messages.create(
            from_='+15864602797',
            body= userMessage,
            to='+919334717500'
                            )          
        return response(status=status.HTTP_201_CREATED)
    else:
        return redirect("/")
         