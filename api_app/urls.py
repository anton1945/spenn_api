from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('transaction/', views.transaction_request, name='transaction_request'),
    path('check_status/', views.check_status, name='check_status'),
    path('callback/', views.callback, name='callback'),
]