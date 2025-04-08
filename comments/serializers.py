from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    citoyen_nom = serializers.CharField(source='citoyen.nom', read_only=True)
    citoyen_prenom = serializers.CharField(source='citoyen.prenom', read_only=True)
    created_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M", read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'citoyen',
            'citoyen_nom',
            'citoyen_prenom',
            'ressource',
            'content',
            'is_deleted',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']