from django.urls import path
from app import views

# TEMPLATE TAGGING
app_name = 'app'

urlpatterns = [
    path('about/',views.about,name="about"),
    path('services/',views.services,name='services'),
    path('pricelist/',views.pricelist,name='pricelist'),
    path('galery/',views.galery,name='galery'),
    path('contact/',views.contact,name='contact'),
]
