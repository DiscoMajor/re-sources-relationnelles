import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Message
from users.models import User
from django.utils import timezone

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Vérifier si l'utilisateur est authentifié
        if self.scope['user'].is_anonymous:
            await self.close()
            return

        # Vérifier si l'utilisateur a accès à cette room
        room = await self.get_room()
        if not room:
            await self.close()
            return
            
        # Rejoindre le groupe de chat
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Quitter le groupe de chat
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Recevoir un message du WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        user_id = self.scope['user'].id
        room_id = int(self.room_name)
        
        # Sauvegarder le message dans la base de données
        await self.save_message(user_id, room_id, message)
        
        # Envoyer le message au groupe
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user_id': user_id,
                'username': self.scope['user'].get_full_name() or self.scope['user'].username,
                'timestamp': timezone.now().isoformat(),
            }
        )

    # Recevoir un message du groupe
    async def chat_message(self, event):
        # Envoyer le message au WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'user_id': event['user_id'],
            'username': event['username'],
            'timestamp': event['timestamp'],
        }))
    
    @database_sync_to_async
    def get_room(self):
        try:
            room = Room.objects.get(id=int(self.room_name))
            # Vérifier si l'utilisateur fait partie des participants
            if self.scope['user'] in room.participants.all():
                return room
            return None
        except Room.DoesNotExist:
            return None
            
    @database_sync_to_async
    def save_message(self, user_id, room_id, message):
        user = User.objects.get(id=user_id)
        room = Room.objects.get(id=room_id)
        Message.objects.create(user=user, room=room, value=message)