from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Room, Message
from users.models import User
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.template.loader import render_to_string

@login_required
def index(request):
    return redirect('chat:rooms_list')

@login_required
def rooms_list(request):
    # Obtenir toutes les rooms auxquelles l'utilisateur participe
    rooms = Room.objects.filter(participants=request.user).order_by('-created_at')
    
    context = {
        'rooms': rooms,
    }
    
    # Si c'est une requête AJAX, retourner seulement le contenu
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('chat/rooms_list.html', context, request=request)
        return HttpResponse(html)
    
    # Sinon, retourner la page complète
    return render(request, 'chat/rooms_list.html', context)

@login_required
def chat_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    
    # Vérifier si l'utilisateur est un participant de cette room
    if request.user not in room.participants.all():
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': "Vous n'avez pas accès à cette conversation."}, status=403)
        messages.error(request, "Vous n'avez pas accès à cette conversation.")
        return redirect('chat:rooms_list')
    
    # Récupérer les messages de la room
    room_messages = Message.objects.filter(room=room).order_by('create_at')
    
    # Marquer tous les messages non lus comme lus
    unread_messages = room_messages.filter(is_read=False).exclude(user=request.user)
    unread_messages.update(is_read=True)
    
    context = {
        'room': room,
        'room_messages': room_messages,
    }
    
    # Si c'est une requête AJAX, retourner seulement le contenu
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('chat/room.html', context, request=request)
        return HttpResponse(html)
    
    # Sinon, retourner la page complète
    return render(request, 'chat/room.html', context)

@login_required
def create_room(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        is_group = request.POST.get('is_group') == 'on'
        participant_ids = request.POST.getlist('participants')
        
        if not room_name:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': "Le nom de la conversation est requis."}, status=400)
            messages.error(request, "Le nom de la conversation est requis.")
            return redirect('chat:rooms_list')
            
        if is_group and len(participant_ids) < 2:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': "Un groupe doit avoir au moins 2 participants."}, status=400)
            messages.error(request, "Un groupe doit avoir au moins 2 participants.")
            return redirect('chat:rooms_list')
            
        room = Room.objects.create(name=room_name, is_group=is_group)
        room.participants.add(request.user)  # Ajout du créateur
        
        # Ajouter les participants sélectionnés
        for user_id in participant_ids:
            try:
                user = User.objects.get(id=user_id)
                room.participants.add(user)
            except User.DoesNotExist:
                continue
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'room_id': room.id})
                
        messages.success(request, f"Conversation '{room_name}' créée avec succès.")
        return redirect('chat:room', room_id=room.id)
    
    # Récupérer les amis pour le formulaire
    friends = request.user.amis.all()
    
    context = {
        'friends': friends,
    }
    
    # Si c'est une requête AJAX, retourner seulement le contenu
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('chat/create_room.html', context, request=request)
        return HttpResponse(html)
    
    # Sinon, retourner la page complète
    return render(request, 'chat/create_room.html', context)

@login_required
def create_direct_chat(request, user_id):
    # Vérifier si l'utilisateur existe et est un ami
    other_user = get_object_or_404(User, id=user_id)
    
    if other_user not in request.user.amis.all():
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': "Vous ne pouvez chatter qu'avec vos relations."}, status=403)
        messages.error(request, "Vous ne pouvez chatter qu'avec vos relations.")
        return redirect('chat:rooms_list')
    
    # Vérifier si un chat direct existe déjà
    existing_chat = Room.objects.filter(
        is_group=False,
        participants=request.user
    ).filter(
        participants=other_user
    ).first()
    
    if existing_chat:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'room_id': existing_chat.id})
        return redirect('chat:room', room_id=existing_chat.id)
    
    # Créer un nouveau chat direct
    room_name = f"{request.user.first_name} et {other_user.first_name}"
    room = Room.objects.create(name=room_name, is_group=False)
    room.participants.add(request.user, other_user)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'room_id': room.id})
    
    messages.success(request, f"Conversation avec {other_user.first_name} créée.")
    return redirect('chat:room', room_id=room.id)

@login_required
def get_unread_count(request):
    # Compter les messages non lus pour l'utilisateur
    unread_count = Message.objects.filter(
        room__participants=request.user,
        is_read=False
    ).exclude(user=request.user).count()
    
    return JsonResponse({'unread_count': unread_count})

@login_required
def mark_messages_read(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    
    # Vérifier si l'utilisateur est un participant de cette room
    if request.user not in room.participants.all():
        return JsonResponse({'error': 'Non autorisé'}, status=403)
    
    # Marquer tous les messages comme lus
    Message.objects.filter(
        room=room,
        is_read=False
    ).exclude(user=request.user).update(is_read=True)
    
    return JsonResponse({'success': True})

@login_required
def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    
    # Vérifier si l'utilisateur est un participant de cette room
    if request.user not in room.participants.all():
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': "Vous n'avez pas accès à cette conversation."}, status=403)
        messages.error(request, "Vous n'avez pas accès à cette conversation.")
        return redirect('chat:rooms_list')
    
    # Supprimer la room
    room_name = room.name
    room.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': f"Conversation '{room_name}' supprimée."})
    
    messages.success(request, f"Conversation '{room_name}' supprimée.")
    return redirect('chat:rooms_list')
