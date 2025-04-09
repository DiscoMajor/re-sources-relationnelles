from django.urls import path
from .views import RessourceCreateView, RessourceListView

app_name = 'ressources'

urlpatterns = [
    path('add/', RessourceCreateView.as_view(), name='add'),
    path('', RessourceListView.as_view(), name='list'),
]