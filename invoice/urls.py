from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^invoice/', views.invoice, name="invoice"),
    url(r'^ajax/get_products/$', views.get_products, name='get_products'),
    url(r'^ajax/get_city/$', views.get_city, name='get_city'),
]
