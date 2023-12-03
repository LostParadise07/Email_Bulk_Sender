from django.urls import path
from .views import  ContactPageView, DocumentationPageView
from django.contrib.auth import views
from . import views
app_name = 'navbar'

urlpatterns = [
    path('', views.MainPageView, name='mainpage'),
    path('mainpage.html', views.MainPageView, name='mainpage.html'),
    path('sendemails.html', views.sendemails, name='sendemails.html'),
    # path("", views.user_home, name="profile"),
    path('contactus/', ContactPageView.as_view(), name='contactus'),
    path('documentation/', DocumentationPageView.as_view(), name='documentation'),
]