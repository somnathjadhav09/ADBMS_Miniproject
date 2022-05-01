"""adbms_mini_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('create_trader/', views.create_trader, name="create_trader"),
    path('traders/', views.list_traders, name="list_traders"),
    path('update_trader_<str:obj_id>/', views.update_trader, name="update_trader"),
    path('delete_trader_<str:obj_id>/', views.delete_trader, name="delete_trader"),

    path('create_uom/', views.create_uom, name="create_uom"),
    path('uoms/', views.list_uoms, name="list_uoms"),
    path('update_uom_<str:obj_id>/', views.update_uom, name="update_uom"),
    path('delete_uom<str:obj_id>/', views.delete_uom, name="delete_uom"),

    path('create_invoice/', views.create_invoice, name="create_invoice"),
    path('invoices/', views.list_invoices, name="list_invoices"),
    path('update_invoice_<str:obj_id>/', views.update_invoice, name="update_invoice"),
    path('delete_invoice<str:obj_id>/', views.delete_invoice, name="delete_invoice"),

    path('create_material/', views.create_material, name="create_material"),
    path('materials/', views.list_materials, name="list_materials"),
    path('update_material_<str:obj_id>/', views.update_material, name="update_material"),
    path('delete_material_<str:obj_id>/', views.delete_material, name="delete_material"),

    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('', views.login, name="index"),
    path('logout/', views.logout, name="logout"),
]
