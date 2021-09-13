from django.urls import path

from . import views 

urlpatterns = [ 
    path('', views.IndexView.as_view(),name='index'),
    path('order_momo/', views.order_momo, name='order_momo'),
    path('order_progress/<str:order_token>/', views.order_progress, name='order_progress'),

]