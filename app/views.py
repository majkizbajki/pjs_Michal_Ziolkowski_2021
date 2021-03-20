from django.shortcuts import render
from app.models import News

# Create your views here.
def index(request):
    news_info = News.objects.order_by('date')
    news_dict = {'newsinfo':news_info}
    return render(request,'app/index.html',context=news_dict)

def about(request):
    return render(request,'app/about.html')

def services(request):
    return render(request,'app/services.html')

def pricelist(request):
    return render(request,'app/pricelist.html')

def galery(request):
    return render(request,'app/galery.html')

def contact(request):
    return render(request,'app/contact.html')
