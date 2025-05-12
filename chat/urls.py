from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),
    path('rooms/', views.rooms_list, name='rooms_list'),
    path('room/<int:room_id>/', views.chat_room, name='room'),
    path('create/', views.create_room, name='create_room'),
    # path('create/<int:user_id>/', views.create_direct_chat, name='create_direct_chat'),
    path('unread-count/', views.get_unread_count, name='unread_count'),
    path('mark-read/<int:room_id>/', views.mark_messages_read, name='mark_read'),
    path('delete/<int:room_id>/', views.delete_room, name='delete_room'),
]