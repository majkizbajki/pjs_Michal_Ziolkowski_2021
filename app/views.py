from django.shortcuts import render, redirect
from app.models import News, Services, UserProfileInfo, Event, Workers
from app.forms import UserForm, UserProfileInfoForm
from app.models import User

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

import datetime
from calendar import HTMLCalendar
from app.utils import Calendar, cal

from django.core.mail import send_mail

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
        if (User.objects.filter(email=request_email).count() == 0 or user.email == request_email) and ("@" in request_email and "." in request_email):
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

            if len(new_password) > 0:
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
                error += "Hasło musi zawierać conajmniej jeden znak."
        else:
            error += "Wprowadzone hasło nie jest zgodne z obecnym. "
            error_type = 1

    return render(request,"app/change_password.html",{"error":error,
                                                      "error_type":error_type})

def show_events(request):

    events = Event.objects.filter(patient_username=request.user.username)
    events_number = Event.objects.filter(patient_username=request.user.username).count()

    if request.method == "POST":
        request_event_number = request.POST.get("event_number")
        events[int(request_event_number)].delete()
        return redirect("/profile/show_events")

    return render(request,"app/show_events.html",{"events":events,"events_number":events_number})

def actuallCalendar(request):
    cal.actuall_day = datetime.date.today().day
    cal.actuall_month = datetime.date.today().month
    cal.actuall_month_string = cal.months[cal.actuall_month]
    cal.actuall_year = datetime.date.today().year

    return calendarView(request)

def calendarView(request):
    actuall_day = cal.actuall_day
    actuall_month = cal.actuall_month
    actuall_month_string = cal.actuall_month_string
    actuall_year = cal.actuall_year

    tc= HTMLCalendar(firstweekday=0)

    type = str(Services.objects.all()[0].name)

    return render(request,"app/calendar.html",{"actuall_day":actuall_day,
                                               "actuall_month":actuall_month,
                                               "actuall_month_string":actuall_month_string,
                                               "actuall_year":actuall_year,
                                               "HTML_Calendar":tc.formatmonth(actuall_year, actuall_month),
                                               "type": type,
                                               })

def increase_month(request):
    cal.increase_month()
    return calendarView(request)

def decrease_month(request):
    cal.decrease_month()
    return calendarView(request)

def reservation(request,year,month,day,type):

    u = request.user
    user = User.objects.get(username=u.username)
    services = Services.objects.all()

    year = str(year)
    month = str(month)
    if len(month)==1:
        month = "0"+str(month)
    day = str(day)
    if len(day)==1:
        day = "0"+str(day)

    actuall_date = year+"-"+month+"-"+day
    events = Event.objects.filter(date=actuall_date);
    events_type = type

    available_hours = {1:"9:00:00",2:"10:00:00",3:"11:00:00",4:"12:00:00",5:"13:00:00",6:"14:00:00",7:"15:00:00",8:"16:00:00"}

    for j in events:
        if j.queue in available_hours and str(j.service) == type:
            available_hours.pop(j.queue)

    if request.method == "POST":
        if request.POST.get("available_hours")!=None:
            request_service = request.POST.get("services")
            service_object = Services.objects.filter(name=request_service).first()

            request_actuall_date = request.POST.get("actuall_date")
            request_actuall_date = datetime.datetime.strptime(request_actuall_date,'%Y-%m-%d')

            request_available_hours = request.POST.get("available_hours")
            request_time = datetime.datetime.strptime(request_available_hours,'%H:%M:%S')

            request_fullname = user.first_name+" "+user.last_name

            get_key = 0
            for key, value in available_hours.items():
                if request_available_hours == value:
                    get_key = key

            new_event = Event(service=service_object,patient_fullname=request_fullname,patient_username=u.username,date=request_actuall_date,time=request_time,queue=get_key)
            new_event.save()

            send_mail(
                'Potwierdzenie rezerwacji w Opti+',
                'Twoja rezerwacja ('+request_service+') w dniu '+str(request_actuall_date)[:10]+' o godzinie '+request_available_hours+' została potwierdzona.',
                'optipluspl@gmail.com',
                [str(user.email)],
                )

            return redirect("/profile/calendar")

    return render(request,"app/reservation.html",{"actuall_date":actuall_date,
                                                  "available_hours":available_hours.values(),
                                                  "services":services,
                                                  "type": events_type,
                                                  })
