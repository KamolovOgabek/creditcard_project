from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('spending/', views.spending, name='spending'),
    path('balance/', views.balance, name='balance'),
    path('customers/', views.customers, name='customers'),
    path('upload/', views.upload_file, name='upload_file'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]
