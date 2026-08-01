from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('how-it-works/', views.how_it_works, name='how_it_works'),
    path('sustainability/', views.sustainability, name='sustainability'),
    path('about-us/', views.about_us, name='about_us'),

]
