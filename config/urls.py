"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path ,include
from django.conf import settings
from django.conf.urls.static import static
from azbankgateways.urls import az_bank_gateways_urls 
from payments.views import callback_gateway_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bankgateways/', az_bank_gateways_urls()),
    path('callback-gateways/',callback_gateway_view ,name='callback-gateways'),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/',include('orders.urls', namespace = 'orders')),
    path('', include('shop.urls', namespace='shop')),
    path('payments/', include('payments.urls', namespace='payments')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                         document_root=settings.MEDIA_ROOT)
