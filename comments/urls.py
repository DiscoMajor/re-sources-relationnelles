from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('<int:ressource_pk>/', views.CommentListView.as_view(), name='list'),
    path('<int:ressource_pk>/add/', views.CommentCreateView.as_view(), name='add'),
    path('<int:pk>/edit/', views.CommentUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.CommentDeleteView.as_view(), name='delete'),
]