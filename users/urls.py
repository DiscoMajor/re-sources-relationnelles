from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('info/', views.info, name='info'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.profile_view, name='profile'),
]