from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^invoice/', views.invoice, name="invoice"),
    url(r'^conexion/', views.conexion, name="conexion"),
    url(r'^register_client/', views.register_client, name="register_client"),
    url(r'^register_salesperson/', views.register_salesperson, name="register_salesperson"),
    url(r'^register_product/', views.register_product, name="register_product"),
    url(r'^ajax/get_products/$', views.get_products, name='get_products'),
    url(r'^ajax/get_city/$', views.get_city, name='get_city'),
]
