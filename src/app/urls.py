from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('search/', views.search, name='search'),
    path('tickets/<str:pk>/', views.tickets, name='tickets'),
    path('create/', views.create_ticket, name='create'),
    path('update/<str:pk>/', views.update_ticket, name='update'),
    path('close/<str:pk>/', views.close, name='close'),
    path('stats/<str:pk>/', views.stats, name='stats'),
]