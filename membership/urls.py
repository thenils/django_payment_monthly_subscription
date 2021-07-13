from django.urls import path
from .views import Home, Plans, checkout


urlpatterns = [
    path('', Home, name='home'),
    path('pricing/', Plans, name='pricing'),
    path('checkout/<str:slug>/', checkout, name='checkout'),

]
