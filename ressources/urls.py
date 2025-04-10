from django.urls import path
from .views import RessourceListView, RessourceCreateView, RessourceDetailView, RessourceDeleteView

app_name = 'ressources'
urlpatterns = [
    path('', RessourceListView.as_view(), name='list'),
    path('add/', RessourceCreateView.as_view(), name='add'),
    path('<int:pk>/', RessourceDetailView.as_view(), name='detail'),
    path('<int:pk>/delete/', RessourceDeleteView.as_view(), name='delete'),
]