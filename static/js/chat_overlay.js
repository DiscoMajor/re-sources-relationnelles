document.addEventListener('DOMContentLoaded', function() {
    // Éléments DOM
    const chatOverlay = document.getElementById('chat-overlay');
    const roomsListView = document.getElementById('rooms-list-view');
    const createRoomView = document.getElementById('create-room-view');
    const roomView = document.getElementById('room-view');
    const overlayTitle = document.getElementById('overlay-title');
    
    // WebSocket pour les messages en temps réel
    let chatSocket = null;
    
    // ===== Fonctions de navigation =====
    
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
        try {
            // Charger le contenu du formulaire via AJAX si pas déjà chargé
            if (createRoomView.innerHTML.trim() === '') {
                const response = await fetch('/chat/create/', {
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });
                
                if (!response.ok) throw new Error('Erreur lors du chargement du formulaire');
                
                const html = await response.text();
                createRoomView.innerHTML = html;
                
                // Ajouter les gestionnaires d'événements au formulaire
                const form = createRoomView.querySelector('form');
                form.addEventListener('submit', handleCreateRoomSubmit);
                
                // Faire en sorte que le bouton Annuler retourne à la liste des conversations
                const cancelBtn = createRoomView.querySelector('a[href="/chat/rooms/"]');
                if (cancelBtn) {
                    cancelBtn.addEventListener('click', function(e) {
                        e.preventDefault();
                        showRoomsList();
                    });
                }
            }
            
            // Afficher la vue
            roomsListView.classList.add('hidden');
            createRoomView.classList.remove('hidden');
            roomView.classList.add('hidden');
            overlayTitle.textContent = 'Nouveau Groupe';
        } catch (error) {
            console.error('Erreur:', error);
            alert('Une erreur est survenue lors du chargement du formulaire');
        }
    }
    
// Afficher une conversation
async function showRoom(roomId) {
    try {
        // Charger le contenu de la conversation via AJAX
        const response = await fetch(`/chat/room/${roomId}/`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });
        
        if (!response.ok) throw new Error('Erreur lors du chargement de la conversation');
        
        const html = await response.text();
        roomView.innerHTML = html;
        
        // Afficher la vue
        roomsListView.classList.add('hidden');
        createRoomView.classList.add('hidden');
        roomView.classList.remove('hidden');
        
        // Marquer les messages comme lus
        markMessagesAsRead(roomId);
        
        // Configurer le WebSocket
        setupWebSocket(roomId);
        
        // Ajouter un bouton de retour si nécessaire
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
                    
                    try {
                        const response = await fetch(`/chat/delete/${roomId}/`, {
                            headers: {
                                'X-Requested-With': 'XMLHttpRequest'
                            }
                        });
                        
                        if (!response.ok) {
                            const errorData = await response.json();
                            throw new Error(errorData.error || 'Erreur lors de la suppression de la conversation');
                        }
                        
                        const data = await response.json();
                        
                        if (data.success) {
                            // Retourner à la liste des conversations après la suppression
                            await loadChatRooms(); // Recharger la liste pour qu'elle soit à jour
                            showRoomsList();
                            
                            // Afficher un message de confirmation (optionnel)
                            alert(data.message || 'Conversation supprimée avec succès');
                        } else {
                            alert(data.error || 'Une erreur est survenue');
                        }
                    } catch (error) {
                        console.error('Erreur:', error);
                        alert(error.message || 'Une erreur est survenue lors de la suppression de la conversation');
                    }
                }
            });
        }
        
        // Intercepter le formulaire d'envoi de message
        const chatForm = roomView.querySelector('#chat-form');
        if (chatForm) {
            chatForm.addEventListener('submit', handleChatFormSubmit);
        }
        
        // Faire défiler jusqu'au dernier message
        scrollToBottom();
    } catch (error) {
        console.error('Erreur:', error);
        alert('Une erreur est survenue lors du chargement de la conversation');
    }
}
    
    // ===== Gestionnaires d'événements =====
    
    // Gérer la soumission du formulaire de création de conversation
    async function handleCreateRoomSubmit(event) {
        event.preventDefault();
        
        try {
            const form = event.target;
            const formData = new FormData(form);
            
            const response = await fetch('/chat/create/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Erreur lors de la création du groupe');
            }
            
            const data = await response.json();
            
            if (data.success) {
                // Recharger la liste des conversations et l'afficher
                await loadChatRooms();
                showRoomsList();
            } else {
                alert(data.error || 'Une erreur est survenue');
            }
        } catch (error) {
            console.error('Erreur:', error);
            alert(error.message || 'Une erreur est survenue lors de la création du groupe');
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
    
    // ===== Fonctions utilitaires =====
    
    // Charger la liste des conversations
    async function loadChatRooms() {
        try {
            const response = await fetch('/chat/rooms/', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            
            if (!response.ok) throw new Error('Erreur lors du chargement des conversations');
            
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
            
            // Ajouter des gestionnaires d'événements pour les boutons de suppression
            const deleteButtons = roomsListView.querySelectorAll('#delete-room-btn');
            deleteButtons.forEach(button => {
                button.addEventListener('click', async function(e) {
                    e.preventDefault();
                    e.stopPropagation(); // Empêcher la propagation du clic vers le lien parent
                    
                    // Confirmation avant suppression
                    if (confirm('Êtes-vous sûr de vouloir supprimer cette conversation ? Cette action est irréversible.')) {
                        const roomId = this.getAttribute('data-room-id');
                        
                        try {
                            const response = await fetch(`/chat/delete/${roomId}/`, {
                                headers: {
                                    'X-Requested-With': 'XMLHttpRequest'
                                }
                            });
                            
                            if (!response.ok) {
                                const errorData = await response.json();
                                throw new Error(errorData.error || 'Erreur lors de la suppression de la conversation');
                            }
                            
                            const data = await response.json();
                            
                            if (data.success) {
                                // Recharger la liste après suppression
                                await loadChatRooms();
                                
                                // Afficher un message de confirmation (optionnel)
                                alert(data.message || 'Conversation supprimée avec succès');
                            } else {
                                alert(data.error || 'Une erreur est survenue');
                            }
                        } catch (error) {
                            console.error('Erreur:', error);
                            alert(error.message || 'Une erreur est survenue lors de la suppression de la conversation');
                        }
                    }
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
        } catch (error) {
            console.error('Erreur lors du chargement des conversations:', error);
            roomsListView.innerHTML = '<div class="text-center py-10"><p class="text-red-500">Erreur lors du chargement des conversations.</p></div>';
        }
    }
    
    // Marquer les messages comme lus
    async function markMessagesAsRead(roomId) {
        try {
            await fetch(`/chat/mark-read/${roomId}/`);
            // Mettre à jour le compteur de messages non lus
            checkUnreadMessages();
        } catch (error) {
            console.error('Erreur lors du marquage des messages comme lus:', error);
        }
    }
    
    // Vérifier les messages non lus
    async function checkUnreadMessages() {
        try {
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
        } catch (error) {
            console.error('Erreur lors de la vérification des messages non lus:', error);
        }
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
            console.error('Chat socket closed unexpectedly');
            // Essayer de se reconnecter après 5 secondes
            setTimeout(function() {
                if (roomView.classList.contains('hidden')) return;
                setupWebSocket(roomId);
            }, 5000);
        };
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
        
        // Créer le HTML du message - Utiliser les nouvelles classes CSS
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
        
        // Faire défiler jusqu'au dernier message
        scrollToBottom();
    }
    
    // Faire défiler jusqu'au dernier message
    function scrollToBottom() {
        const messageContainer = document.querySelector('#message-container');
        if (messageContainer) {
            messageContainer.scrollTop = messageContainer.scrollHeight;
        }
    }
    
    // ===== Initialisation =====
    
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
    
    // Ajouter des gestionnaires d'événements pour les boutons
    if (document.querySelector('a[href="/chat/rooms/"]')) {
        document.querySelectorAll('a[href="/chat/rooms/"]').forEach(link => {
            link.addEventListener('click', function(e) {
                // Seulement si on n'est pas déjà sur une page de chat
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
    
    // Vérifier les messages non lus toutes les 30 secondes
    checkUnreadMessages();
    setInterval(checkUnreadMessages, 30000);

    // Fonctions pour la gestion d'une room individuelle
    function setupRoomFunctions(roomId, userId, userName) {
        // Scroll to bottom of message container
        function scrollToBottom() {
            const messageContainer = document.getElementById('message-container');
            if (messageContainer) {
                messageContainer.scrollTop = messageContainer.scrollHeight;
            }
        }
        
        // Add message to chat
        function addMessage(message, user_id, username, timestamp) {
            const messageContainer = document.getElementById('message-container');
            if (!messageContainer) return;
            
            const isMyMessage = user_id === userId;
            
            // Format timestamp
            const date = new Date(timestamp);
            const hours = date.getHours().toString().padStart(2, '0');
            const minutes = date.getMinutes().toString().padStart(2, '0');
            
            // Create message HTML
            const messageDiv = document.createElement('div');
            messageDiv.className = `mb-4 flex ${isMyMessage ? 'justify-end' : ''}`;
            
            const messageBubble = document.createElement('div');
            messageBubble.className = `message-bubble p-3 ${isMyMessage ? 'my-message' : 'other-message'}`;
            
            // Add sender name for group chats if not my message
            const isGroup = document.querySelector('div[data-is-group="true"]') !== null;
            if (!isMyMessage && isGroup) {
                const nameElement = document.createElement('p');
                nameElement.className = 'text-xs text-gray-600 mb-1';
                nameElement.textContent = username;
                messageBubble.appendChild(nameElement);
            }
            
            // Message content
            const messageContent = document.createElement('p');
            messageContent.className = 'text-gray-800';
            messageContent.textContent = message;
            messageBubble.appendChild(messageContent);
            
            // Timestamp
            const timeElement = document.createElement('p');
            timeElement.className = 'text-xs text-gray-500 text-right mt-1';
            timeElement.textContent = `${hours}:${minutes}`;
            messageBubble.appendChild(timeElement);
            
            messageDiv.appendChild(messageBubble);
            messageContainer.appendChild(messageDiv);
            
            // Scroll to the latest message
            scrollToBottom();
        }
        
        // Connect to WebSocket
        function connectWebSocket() {
            const chatSocket = new WebSocket(
                'ws://' + window.location.host + '/ws/chat/' + roomId + '/'
            );

            chatSocket.onmessage = function(e) {
                const data = JSON.parse(e.data);
                addMessage(data.message, data.user_id, data.username, data.timestamp);
            };

            chatSocket.onclose = function(e) {
                console.error('Chat socket closed unexpectedly');
                // Try to reconnect in 5 seconds
                setTimeout(function() {
                    connectWebSocket();
                }, 5000);
            };
            
            return chatSocket;
        }
        
        // Marquer les messages comme lus
        async function markMessagesAsRead() {
            try {
                await fetch(`/chat/mark-read/${roomId}/`);
            } catch (error) {
                console.error('Erreur lors du marquage des messages comme lus:', error);
            }
        }
        
        // Initialiser la room
        function initRoom() {
            let chatSocket = null;
            
            // Connect to WebSocket
            chatSocket = connectWebSocket();
            
            // Scroll to bottom when page loads
            scrollToBottom();
            
            // Marquer les messages comme lus
            markMessagesAsRead();
            
            // Handle form submission
            const chatForm = document.getElementById('chat-form');
            if (chatForm) {
                chatForm.addEventListener('submit', function(e) {
                    e.preventDefault();
                    
                    const messageInput = document.getElementById('message-input');
                    const message = messageInput.value.trim();
                    
                    if (message && chatSocket && chatSocket.readyState === WebSocket.OPEN) {
                        chatSocket.send(JSON.stringify({
                            'message': message
                        }));
                        
                        messageInput.value = '';
                    }
                    
                    messageInput.focus();
                });
            }
        }
        
        // Lancer l'initialisation
        initRoom();
    }

    // Étendre la fonction showRoom pour initialiser la room
    function enhanceShowRoom(originalShowRoom) {
        return async function(roomId) {
            // Appeler la fonction originale
            await originalShowRoom(roomId);
            
            // Récupérer les données utilisateur
            const metaUserId = document.querySelector('meta[name="user-id"]');
            const userId = metaUserId ? parseInt(metaUserId.content) : 0;
            const userName = document.querySelector('meta[name="user-name"]')?.content || '';
            
            // Initialiser les fonctions spécifiques à la room
            setupRoomFunctions(roomId, userId, userName);
            
            // Mise à jour du titre de l'overlay
            const conversationName = roomView.querySelector('.text-lg.font-medium.text-gray-900')?.textContent;
            if (conversationName && overlayTitle) {
                overlayTitle.textContent = conversationName;
            }
        };
    }

    // Surcharger la fonction showRoom une fois que le DOM est chargé
    document.addEventListener('DOMContentLoaded', function() {
        // Vérifier si la fonction showRoom existe
        if (typeof window.showRoom === 'function') {
            // Sauvegarder la fonction originale
            const originalShowRoom = window.showRoom;
            
            // Remplacer par la version améliorée
            window.showRoom = enhanceShowRoom(originalShowRoom);
        }
    });
});