from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.conf.urls import url

app_name = 'basicapp'

urlpatterns  = [
    path("",views.index,name='index'),
    path("register",views.register, name="register"),
    path("login",views.login,name="login"),
    path("logout",views.logout,name="logout"),
    path("fare",views.fare,name="fare"),
    path('rent_now',views.rent_now,name="rent_now"),
    path('contact',views.contact,name='contact'),
    path('mybookings',views.mybookings,name='mybookings'),
    path('bicycle',views.bicycle,name='bicycle'),
    path('discount',views.mydiscount,name='discount'),
    url(r'changepass', views.change_password, name='change_password'),
    path('accessories',views.myaccessories,name='accessories'),
    path('search',views.search,name='search'),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)