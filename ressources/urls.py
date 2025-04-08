from django.urls import path
from .views import RessourceCreateView

app_name = 'ressources'

urlpatterns = [
    path('add/', RessourceCreateView.as_view(), name='add'),
]