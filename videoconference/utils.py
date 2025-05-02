import os
import jwt
import time

def create_livekit_token(identity: str, room: str = 'default'):
    """
    Génère un JWT pour l'accès à une salle LiveKit.

    :param identity: L'identité de l'utilisateur (ex : son nom ou ID)
    :param room: La salle cible (par défaut 'default')
    :return: Un token JWT LiveKit signé
    """

    api_key = os.getenv("LIVEKIT_API_KEY")
    api_secret = os.getenv("LIVEKIT_API_SECRET")

    # Payload exigé par LiveKit
    payload = {
        "iss": api_key,         # L'émetteur (clé API)
        "sub": identity,        # Identité de l'utilisateur
        "room": room,
        "video": True,          # Permissions
        "audio": True,
        "exp": int(time.time()) + 3600,  # Expiration (1h)
    }

    token = jwt.encode(payload, api_secret, algorithm="HS256")
    return token