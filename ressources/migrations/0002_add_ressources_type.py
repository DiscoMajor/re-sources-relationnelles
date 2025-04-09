from django.db import migrations

def create_ressources_types(apps, schema_editor):
    Type = apps.get_model('ressources', 'Type')

    types = [
    {'label': 'Activité'},
    {'label': 'Article'},
    {'label': 'Carte défi'},
    {'label': 'Cours au format PDF'},
    {'label': 'Exercice'},
    {'label': 'Fiche de lecture'},
    {'label': 'Jeu en ligne'},
    {'label': 'Vidéo'},
    ]

    for type in types:
        Type.objects.create(**type)
class Migration(migrations.Migration):

    dependencies = [
        ('ressources', '0001_initial'),
    ]

    operations = [migrations.RunPython(create_ressources_types)]
