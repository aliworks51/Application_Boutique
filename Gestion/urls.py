from django.urls import path
from . import views

urlpatterns = [
    path('dash_admin/', views.dash_admin, name='dash_admin'),
  ]
