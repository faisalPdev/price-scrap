from django.contrib import admin
from django.urls import path,include
from .import views


urlpatterns = [
    path('',views.home,name='home'),
    path('signin',views.signin,name='signin'),
    path('signup',views.signup,name='signup'),
    path('about',views.about,name='about'),
    path('contactus',views.contactus,name='contactus'),
    path('userview',views.userview,name='userview'),
    path('logout',views.Logoutpage,name='logout'),
    path('tracking',views.tracking,name='tracking'),
    path('searchHistory',views.search,name='search'),
   path('trackHistory',views.trackHistory,name='trackHistory'),

]