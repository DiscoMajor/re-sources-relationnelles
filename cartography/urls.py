from django.urls import path
from . import views

app_name = 'cartography'

urlpatterns = [
    path('', views.map_view, name='map'),
    path('save-address-search/', views.save_address_search, name='save_address_search'),
    path('search-address/', views.search_address_view, name='search_address'),
]