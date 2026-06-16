"""
URL configuration for Nelcay project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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


from system import views
from system.views import MpesaClient

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('contact.html/', views.contact, name='contact'),
    path('about.html/', views.about, name='about'),
    path('gallery.html/', views.gallery, name='gallery'),
    path('pricing.html/',views.pricing, name='pricing'),
    path('payment.html/', views.payment, name='payment'),
    path('mpesaapi/', views.mpesaapi, name='mpesaapi'),
    path('add/', views.add, name='add'),
    path('order.html/', views.order_view, name='order'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('edit/', views.edit, name='edit'),
    path('baker_portal/', views.baker_portal, name='baker_portal'),
    path('update-order/<int:order_id>/', views.update_order, name='update_order'),
    path('mpesa/callback', views.mpesa_callback, name='mpesa_callback'),
    path('paymentprocessing/', views.payment_processing, name='payment_processing'),
    path('check-status/', views.check_payment_status, name='check_payment_status'),

]
