# Module de Visioconférence

Ce module permet la gestion de visioconférences dans l'application Re-Sources Relationnelles en utilisant l'API Jitsi Meet.

## Fonctionnalités

- Création de réunions programmées
- Gestion des réunions (titre, date/heure, durée)
- Interface de visioconférence intégrée
- Partage de liens de réunion
- Statuts des réunions (à venir, en cours, terminée)

## Installation

1. Ajoutez 'visio' à INSTALLED_APPS dans settings.py :
```python
INSTALLED_APPS = [
    ...
    'visio',
]
```

## Structure du Module

```
visio/
├── migrations/          # Migrations de base de données
├── templates/visio/     # Templates HTML
│   ├── home.html       # Page de création de réunion
│   ├── meeting_list.html # Liste des réunions
│   ├── video_call.html  # Interface de visioconférence
│   └── guest.html      # Vue invité
├── models.py           # Modèle Meeting
├── forms.py           # Formulaire de création
├── views.py           # Logique des vues
└── urls.py            # Configuration des URLs
```

## Modèle de Données

Le modèle `Meeting` comprend :
- Créateur (ForeignKey vers User)
- Titre de la réunion
- Date et heure de début
- Durée
- Identifiant unique
- Statut (calculé automatiquement)

## Utilisation

### Créer une Réunion
1. Accédez à l'interface de création
2. Remplissez le formulaire avec :
   - Titre de la réunion
   - Date et heure de début
   - Durée en minutes

### Rejoindre une Réunion
1. Via la liste des réunions
2. Via un lien partagé
3. Interface compatible PC et mobile

## Configuration Jitsi

L'intégration Jitsi est configurée avec :
- Interface en français
- Mode audio/vidéo désactivés par défaut
- Chat et lobby activés
- Contrôles de base (micro, caméra, partage d'écran)

## Sécurité

- Authentification requise pour la création
- Liens uniques pour chaque réunion
- Protection contre les accès non autorisés

## Interface Utilisateur

- Design responsive avec Tailwind CSS
- Notifications de copie de lien
- Indicateurs de statut des réunions
- Formulaires avec validation

## Développement

Pour contribuer au développement :
1. Fork le projet
2. Créez une branche pour votre fonctionnalité
3. Soumettez une pull request

## Auteurs

- Équipe Re-Sources Relationnelles