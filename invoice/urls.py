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
    url(r'^report_clients/', views.report_clients, name="report_clients"),
    url(r'^report_salespersons/', views.report_salespersons, name="report_salespersons"),
    url(r'^report_products/', views.report_products, name="report_products"),
    url(r'^report_cities/', views.report_cities, name="report_cities"),
    url(r'^dashboard/', views.dashboard, name="dashboard"),
    url(r'^get_city_data/$', views.get_city_data, name='get_city_data'),
    url(r'^get_total_month/$', views.get_total_month, name='get_total_month'),
    url(r'^get_top_products/$', views.get_top_products, name='get_top_products'),
    url(r'^get_top_clients/$', views.get_top_clients, name='get_top_clients'),
    url(r'^get_top_salespersons/$', views.get_top_salespersons, name='get_top_salespersons'),
]
