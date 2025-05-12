document.addEventListener('DOMContentLoaded', function() {
    // Éléments DOM
    const chatOverlay = document.getElementById('chat-overlay');
    const roomsListView = document.getElementById('rooms-list-view');
    const createRoomView = document.getElementById('create-room-view');
    const roomView = document.getElementById('room-view');
    const overlayTitle = document.getElementById('overlay-title');
    // WebSocket pour les messages en temps réel
    let chatSocket = null;

    // Afficher la liste des conversations
    function showRoomsList() {
        roomsListView.classList.remove('hidden');
        createRoomView.classList.add('hidden');
        roomView.classList.add('hidden');
        overlayTitle.textContent = 'Messages';
        // Fermer le WebSocket si ouvert
        if (chatSocket && chatSocket.readyState === WebSocket.OPEN) {
            chatSocket.close();
        }
    }

    // Afficher le formulaire de création de conversation
    async function showCreateRoomForm() {
        // Charger le contenu du formulaire
        if (createRoomView.innerHTML.trim() === '') {
            const response = await fetch('/chat/create/', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            const html = await response.text();
            createRoomView.innerHTML = html;
            // Ajouter les gestionnaires d'événements au formulaire
            const form = createRoomView.querySelector('form');
            form.addEventListener('submit', handleCreateRoomSubmit);
            // Retourner à la liste des conversations en cliquant sur Annuler
            const cancelBtn = createRoomView.querySelector('a[href="/chat/rooms/"]');
            if (cancelBtn) {
                cancelBtn.addEventListener('click', function(e) {
                    e.preventDefault();
                    showRoomsList();
                });
            }
        }

        // Afficher la vue create_room
        roomsListView.classList.add('hidden');
        createRoomView.classList.remove('hidden');
        roomView.classList.add('hidden');
        overlayTitle.textContent = 'Nouveau Groupe';
    }

    // Faire défiler jusqu'au dernier message
    function scrollToBottom() {
        const messageContainer = document.querySelector('#message-container');
        if (messageContainer) {
            messageContainer.scrollTop = messageContainer.scrollHeight;
        }
    }

    // Ajouter un message à la conversation
    function addMessage(message, user_id, username, timestamp) {
        const messageContainer = document.querySelector('#message-container');
        if (!messageContainer) return;

        const userId = parseInt(document.querySelector('meta[name="user-id"]')?.content || '0');
        const isMyMessage = user_id === userId;
        // Formater l'horodatage
        const date = new Date(timestamp);
        const hours = date.getHours().toString().padStart(2, '0');
        const minutes = date.getMinutes().toString().padStart(2, '0');
        // Créer la vue du message
        const messageDiv = document.createElement('div');
        messageDiv.className = `mb-4 flex ${isMyMessage ? 'justify-end' : ''}`;
        const messageBubble = document.createElement('div');
        messageBubble.className = `chat-message-bubble p-3 ${isMyMessage ? 'chat-my-message' : 'chat-other-message'}`;
        // Ajouter le nom de l'expéditeur pour les conversations de groupe
        const isGroup = roomView.querySelector('div[data-is-group="true"]') !== null;
        if (!isMyMessage && isGroup) {
            const nameElement = document.createElement('p');
            nameElement.className = 'text-xs text-gray-600 mb-1';
            nameElement.textContent = username;
            messageBubble.appendChild(nameElement);
        }

        // Contenu du message
        const messageContent = document.createElement('p');
        messageContent.className = 'text-gray-800';
        messageContent.textContent = message;
        messageBubble.appendChild(messageContent);
        // Horodatage
        const timeElement = document.createElement('p');
        timeElement.className = 'text-xs text-gray-500 text-right mt-1';
        timeElement.textContent = `${hours}:${minutes}`;
        messageBubble.appendChild(timeElement);
        messageDiv.appendChild(messageBubble);
        messageContainer.appendChild(messageDiv);
        scrollToBottom();
    }

    // Configurer le WebSocket pour une conversation
    function setupWebSocket(roomId) {
        // Fermer le WebSocket précédent s'il existe
        if (chatSocket && chatSocket.readyState === WebSocket.OPEN) {
            chatSocket.close();
        }
        // Créer un nouveau WebSocket
        chatSocket = new WebSocket(
            'ws://' + window.location.host + '/ws/chat/' + roomId + '/'
        );
        chatSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            addMessage(data.message, data.user_id, data.username, data.timestamp);
        };

        chatSocket.onclose = function(e) {
            // Essayer de se reconnecter après 5 secondes
            setTimeout(function() {
                if (roomView.classList.contains('hidden')) return;
                setupWebSocket(roomId);
            }, 5000);
        };
        return chatSocket;
    }

    // Marquer les messages comme lus
    async function markMessagesAsRead(roomId) {
        await fetch(`/chat/mark-read/${roomId}/`);
        // Mettre à jour le compteur de messages non lus
        checkUnreadMessages();
    }

    // Gérer la soumission du formulaire de création de conversation
    async function handleCreateRoomSubmit(event) {
        event.preventDefault();
        const form = event.target;
        const formData = new FormData(form);
        const response = await fetch('/chat/create/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });

        const data = await response.json();
        if (data.success) {
            // Recharger la liste des conversations et l'afficher
            await loadChatRooms();
            showRoomsList();
        }
    }

    // Gérer la soumission du formulaire de chat
    function handleChatFormSubmit(event) {
        event.preventDefault();
        const messageInput = event.target.querySelector('#message-input');
        const message = messageInput.value.trim();
        if (message && chatSocket && chatSocket.readyState === WebSocket.OPEN) {
            chatSocket.send(JSON.stringify({
                'message': message
            }));
            messageInput.value = '';
        }
        messageInput.focus();
    }

    // Afficher une conversation
    async function showRoom(roomId) {
        const response = await fetch(`/chat/room/${roomId}/`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });

        const html = await response.text();
        roomView.innerHTML = html;
        // Afficher la vue du salon de conversation
        roomsListView.classList.add('hidden');
        createRoomView.classList.add('hidden');
        roomView.classList.remove('hidden');
        // Marquer les messages comme lus
        markMessagesAsRead(roomId);
        // Configurer le WebSocket
        setupWebSocket(roomId);
        // Ajouter un bouton de retour
        const closeBtn = roomView.querySelector('a[href*="/chat/rooms/"]');
        if (closeBtn) {
            closeBtn.href = '#';
            closeBtn.addEventListener('click', function(e) {
                e.preventDefault();
                showRoomsList();
            });
        }

        // Ajouter la gestion du bouton de suppression
        const deleteBtn = roomView.querySelector('#delete-room-btn');
        if (deleteBtn) {
            deleteBtn.addEventListener('click', async function(e) {
                e.preventDefault();
                // Confirmation avant suppression
                if (confirm('Êtes-vous sûr de vouloir supprimer cette conversation ? Cette action est irréversible.')) {
                    const roomId = this.getAttribute('data-room-id');
                    const response = await fetch(`/chat/delete/${roomId}/`, {
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest'
                        }
                    });

                    const data = await response.json();
                    if (data.success) {
                        // Retourner à la liste des conversations après la suppression et recharger la liste pour qu'elle soit à jour
                        await loadChatRooms();
                        showRoomsList();
                        alert(data.message || 'Conversation supprimée avec succès');
                    }
                }
            });
        }

        // Intercepter le formulaire d'envoi de message
        const chatForm = roomView.querySelector('#chat-form');
        if (chatForm) {
            chatForm.addEventListener('submit', handleChatFormSubmit);
        }

        // Mettre à jour le titre de l'overlay avec le nom de la conversation
        const conversationName = roomView.querySelector('.text-lg.font-medium.text-gray-900')?.textContent;
        if (conversationName && overlayTitle) {
            overlayTitle.textContent = conversationName;
        }

        // Faire défiler jusqu'au dernier message
        scrollToBottom();
    }

    // Charger la liste des conversations
    async function loadChatRooms() {
        const response = await fetch('/chat/rooms/', {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });
        const html = await response.text();
        roomsListView.innerHTML = html;
        // Ajouter des gestionnaires d'événements pour les liens de room
        const roomLinks = roomsListView.querySelectorAll('a[href^="/chat/room/"]');
        roomLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                // Extraire l'ID de la room de l'URL
                const roomId = this.getAttribute('href').split('/').filter(Boolean)[2];
                showRoom(roomId);
            });
        });

        // Bouton Nouveau groupe
        const newConversationBtns = roomsListView.querySelectorAll('a[href="/chat/create/"]');
        newConversationBtns.forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                showCreateRoomForm();
            });
        });
    }

    // Vérifier les messages non lus
    async function checkUnreadMessages() {
        const response = await fetch('/chat/unread-count/');
        const data = await response.json();
        const unreadCount = document.getElementById('unread-count');
        const mobileUnreadCount = document.getElementById('mobile-unread-count');
        if (data.unread_count > 0) {
            unreadCount.textContent = data.unread_count;
            unreadCount.classList.remove('hidden');
            mobileUnreadCount.textContent = data.unread_count;
            mobileUnreadCount.classList.remove('hidden');
        } else {
            unreadCount.classList.add('hidden');
            mobileUnreadCount.classList.add('hidden');
        }
    }

    // Ouvrir l'overlay du chat
    function openChatOverlay() {
        loadChatRooms();
        chatOverlay.classList.remove('hidden');
    }

    // Fermer l'overlay du chat
    function closeChatOverlay() {
        chatOverlay.classList.add('hidden');
        // Fermer le WebSocket si ouvert
        if (chatSocket && chatSocket.readyState === WebSocket.OPEN) {
            chatSocket.close();
        }
    }

    // Initialisation des événements
    function initEvents() {
        // Boutons qui ouvrent l'overlay de chat
        if (document.querySelector('a[href="/chat/rooms/"]')) {
            document.querySelectorAll('a[href="/chat/rooms/"]').forEach(link => {
                link.addEventListener('click', function(e) {
                    if (!window.location.pathname.includes('/chat/')) {
                        e.preventDefault();
                        openChatOverlay();
                    }
                });
            });
        }

        // Bouton de fermeture
        if (document.getElementById('close-chat-overlay')) {
            document.getElementById('close-chat-overlay').addEventListener('click', closeChatOverlay);
        }

        // Fermer l'overlay si on clique en dehors
        chatOverlay.addEventListener('click', function(e) {
            if (e.target === chatOverlay) {
                closeChatOverlay();
            }
        });
    }

    function init() {
        initEvents();
        // Vérifier les messages non lus au chargement
        checkUnreadMessages();
        // Vérifier les messages non lus toutes les 30 secondes
        setInterval(checkUnreadMessages, 30000);
    }
    init();
});