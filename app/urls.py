from django.urls import path
from app import views

# TEMPLATE TAGGING
app_name = 'app'

urlpatterns = [
    path('about/',views.about,name="about"),
    path('services/',views.services,name='services'),
    path('services/serviceinfo',views.serviceinfo,name='serviceinfo'),
    path('services/diagnostyka',views.service1,name='service1'),
    path('services/leczenie',views.service2,name='service2'),
    path('services/jaskra',views.service3,name='service3'),
    path('services/zacma',views.service4,name='service4'),
    path('pricelist/',views.serviceslist,name='pricelist'),
    path('galery/',views.galery,name='galery'),
    path('contact/',views.contact,name='contact'),
]
