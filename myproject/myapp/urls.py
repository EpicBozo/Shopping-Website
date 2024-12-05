from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('', views.index, name="home"),
    path('results/', views.get_product_info, name="results"),
    path('sort/', views.sort_price, name="sort"),
    path('range/', views.price_range, name="range"),
]