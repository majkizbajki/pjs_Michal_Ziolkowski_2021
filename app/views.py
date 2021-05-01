from django.shortcuts import render
from app.models import News, Services, UserProfileInfo, Event
from app.forms import UserForm, UserProfileInfoForm
from app.models import User

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

import datetime
from calendar import HTMLCalendar
from app.utils import Calendar, cal

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
    user = User.objects.get(username=u.username)

    obj = UserProfileInfo.objects.get(user=u)

    gender = UserProfileInfo._meta.get_field("gender")
    gender_value = gender.value_from_object(obj)
    phone_number = UserProfileInfo._meta.get_field("phone_number")
    phone_number_value = phone_number.value_from_object(obj)
    birth_date = UserProfileInfo._meta.get_field("birth_date")
    birth_date_value = birth_date.value_from_object(obj)
    error = ""
    error_type = 0

    if request.method == "POST":
        request_first_name = request.POST.get("first_name")
        request_last_name = request.POST.get("last_name")
        request_email = request.POST.get("email")
        request_phone_number = request.POST.get("phone_number")
        request_birth_date = request.POST.get("birth_date")
        request_gender = request.POST.get("gender")
        error = ""
        error_type = 0

        if len(request_first_name)>1:
            user.first_name = request_first_name
        else:
            error += "Niepoprawne imię. "
            error_type = 1
        if len(request_last_name)>1:
            user.last_name = request_last_name
        else:
            error += "Niepoprawne nazwisko. "
            error_type = 1
        if User.objects.filter(email=request_email).count() == 0 or user.email == request_email and "@" in request_email and "." in request_email:
            user.email = request_email
        else:
            error += "Niepoprawny lub już istniejący email. "
            error_type = 1
        if len(request_phone_number) == 9 and request_phone_number.isnumeric():
            obj.phone_number = request_phone_number
            phone_number_value = request_phone_number
        else:
            error += "Niepoprawny numer telefonu. "
            error_type = 1
        obj.birth_date = request_birth_date
        birth_date_value = datetime.date(int(str(request_birth_date)[0]+str(request_birth_date)[1]+str(request_birth_date)[2]+str(request_birth_date)[3]),int(str(request_birth_date)[5]+str(request_birth_date)[6]),int(str(request_birth_date)[8]+str(request_birth_date)[9]))
        obj.gender = request_gender
        gender_value = request_gender

        obj.save()
        user.save()
        if error_type == 0:
            error += "Wprowadzone dane zapisano pomyślnie."
            error_type = 2

    return render(request,"app/personal_data.html",{"first_name_value":user.first_name,
                                                    "last_name_value":user.last_name,
                                                    "email_value":user.email,
                                                    "phone_number_value":phone_number_value,
                                                    "birth_date_value":birth_date_value,
                                                    "gender_value":gender_value,
                                                    "error":error,
                                                    "error_type": error_type})

def change_password(request):
    u = request.user
    user = User.objects.get(username=u.username)
    error = ""
    error_type = 0

    if request.method == "POST":

        current_password = request.POST.get("current")
        new_password = request.POST.get("new")
        repeat_password = request.POST.get("repeat")
        error = ""
        error_type = 0

        if user.check_password(current_password):

            if new_password == repeat_password:

                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)

                error += "Zmiana hasła przebiegła pomyślnie."
                error_type = 2

            else:
                error += "Wpisane hasła różnią się od siebie. "
                error_type = 1
        else:
            error += "Wprowadzone hasło nie jest zgodne z obecnym. "
            error_type = 1

    return render(request,"app/change_password.html",{"error":error,
                                                      "error_type":error_type})

def show_events(request):
    return render(request,"app/show_events.html")

def calendarView(request):
    actuall_day = cal.temp_day
    actuall_month = cal.temp_month
    actuall_month_string = cal.temp_month_string
    actuall_year = cal.temp_year
    tc= HTMLCalendar(firstweekday=0)

    return render(request,"app/calendar.html",{"actuall_day":cal.actuall_day,
                                               "actuall_month":cal.actuall_month,
                                               "actuall_month_string":cal.actuall_month_string,
                                               "actuall_year":cal.actuall_year,
                                               "HTML_Calendar":tc.formatmonth(cal.actuall_year, cal.actuall_month),
                                               })

def increase_month(request):
    cal.temp_day = 1
    cal.increase_month()
    cal.temp_month_string = cal.months[cal.temp_month]
    tc= HTMLCalendar(firstweekday=0)
    return render(request,"app/calendar.html",{"actuall_day":cal.temp_day,
                                               "actuall_month":cal.temp_month,
                                               "actuall_month_string":cal.temp_month_string,
                                               "actuall_year":cal.temp_year,
                                               "HTML_Calendar":tc.formatmonth(cal.temp_year, cal.temp_month),
                                               })

def decrease_month(request):
    cal.temp_day = 1
    cal.decrease_month()
    cal.temp_month_string = cal.months[cal.temp_month]
    tc= HTMLCalendar(firstweekday=0)
    return render(request,"app/calendar.html",{"actuall_day":cal.temp_day,
                                               "actuall_month":cal.temp_month,
                                               "actuall_month_string":cal.temp_month_string,
                                               "actuall_year":cal.temp_year,
                                               "HTML_Calendar":tc.formatmonth(cal.temp_year, cal.temp_month),
                                               })

def reservation(request):
    return render(request,"app/reservation.html",{})
