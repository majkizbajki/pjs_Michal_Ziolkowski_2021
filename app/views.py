from django.shortcuts import render
from app.models import News, Services

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
