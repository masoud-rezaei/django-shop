from django.urls import path
from .views import go_to_gateway_view, payment_canceled , payment_done

app_name = 'payments'    
    
urlpatterns = [
    path('go-to-gateways/',go_to_gateway_view ,name='go-to-gateways'),
   # path('callback-gateways/',callback_gateway_view ,name='callback-gateways'),
    path('done/',payment_done, name='done'),
    path('canceled/',payment_canceled, name='canceled'),
]
    
    
   