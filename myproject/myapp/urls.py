from django.contrib import admin
from django.urls import path
from myapp import views
from account_handling import views as account_views

urlpatterns = [
    path('', views.index, name="home"),
    path('results/', views.get_product_info_view, name="results"),
    path('sort/', views.sort_price, name="sort"),
    path('range/', views.price_range, name="range"),
    path('login/', account_views.login, name="login"),
    path('signup/', account_views.signup, name="sign-up"),
]