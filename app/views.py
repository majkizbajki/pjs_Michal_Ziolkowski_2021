from django.shortcuts import render
from app.models import News, Services, UserProfileInfo
from app.forms import UserForm, UserProfileInfoForm

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    news_info = News.objects.order_by('date')
    news_dict = {'newsinfo':news_info}
    return render(request,'app/index.html',context=news_dict)

def about(request):
    return render(request,'app/about.html')

def services(request):
    return render(request,'app/services.html')

def serviceinfo(request):
    return render(request,'app/serviceinfo.html')

def service1(request):
    return render(request,'app/service1.html')

def service2(request):
    return render(request,'app/service2.html')

def service3(request):
    return render(request,'app/service3.html')

def service4(request):
    return render(request,'app/service4.html')

def serviceslist(request):
    price_info_d = Services.objects.filter(service_type=2) #id = 2 - Diagnostyka in data base table
    price_info_l = Services.objects.filter(service_type=1) #id = 1 - Leczenie in data base table
    price_dict = {'priceinfod':price_info_d,'priceinfol':price_info_l}
    return render(request,'app/pricelist.html',context=price_dict)

def galery(request):
    return render(request,'app/galery.html')

def contact(request):
    return render(request,'app/contact.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):

    registered = False
    error = ""

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()

            registered = True
        else:
            if user_form.is_valid() == False:
                error += "Podana nazwa użytkownika lub email już istnieją."
            elif profile_form.is_valid() == False:
                error += "Sprawdź poprawność pól: Płeć, Data urodzenia, Numer telefonu."
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,"app/register.html",{'user_form':user_form,
                                               'profile_form':profile_form,
                                               'registered':registered,
                                               'error':error})


def user_login(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("KONTO NIE ISTNIEJE")
        else:
            error = "Nazwa użytkownika lub hasło są nieprawidłowe!"
            return render(request,"app/login.html",{'error':error})
    else:
        return render(request,"app/login.html",{})

def profile(request):
    return render(request,"app/profile.html");

def personal_data(request):
    u = request.user
    obj = UserProfileInfo.objects.get(user=u)

    gender = UserProfileInfo._meta.get_field("gender")
    gender_value = gender.value_from_object(obj)
    phone_number = UserProfileInfo._meta.get_field("phone_number")
    phone_number_value = phone_number.value_from_object(obj)
    birth_date = UserProfileInfo._meta.get_field("birth_date")
    birth_date_value = birth_date.value_from_object(obj)

    return render(request,"app/personal_data.html",{"first_name_value":u.first_name,
                                                    "last_name_value":u.last_name,
                                                    "email_value":u.email,
                                                    "phone_number_value":phone_number_value,
                                                    "birth_date_value":birth_date_value,
                                                    "gender_value":gender_value});

def change_password(request):
    return render(request,"app/change_password.html");

def show_events(request):
    return render(request,"app/show_events.html");
