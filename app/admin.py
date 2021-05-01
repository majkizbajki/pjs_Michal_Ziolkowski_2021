from django.contrib import admin
from app.models import News,Services,Workers,Servicetypes, UserProfileInfo, Event
# Register your models here.
admin.site.register(News)
admin.site.register(Services)
admin.site.register(Workers)
admin.site.register(Servicetypes)
admin.site.register(UserProfileInfo)
admin.site.register(Event)
