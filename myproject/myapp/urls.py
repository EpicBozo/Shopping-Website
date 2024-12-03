from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('', views.index, name="home"),
    path('results/', views.scraper, name="results"),
    path('sort/', views.sort_price, name="sort")
]