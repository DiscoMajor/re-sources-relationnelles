from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect  # PROD
from django.views.decorators.csrf import csrf_exempt  # TEST
import json
import logging
from .forms import AddressSearchForm
from .models import AddressSearch

logger = logging.getLogger(__name__)

def map_view(request):
    facility_types = [
        {'value': '', 'label': 'Tous les établissements'},
        {'value': 'hospital', 'label': 'Hôpitaux'},
        {'value': 'pharmacy', 'label': 'Pharmacies'},
        {'value': 'doctors', 'label': 'Médecins'},
        {'value': 'clinic', 'label': 'Cliniques'},
    ]
   
    address_form = AddressSearchForm()
   
    return render(request, 'cartography/map.html', {
        'facility_types': facility_types,
        'address_form': address_form
    })

# Utilisez csrf_protect en production
# @csrf_protect
@csrf_exempt  # À utiliser UNIQUEMENT pour les tests
def save_address_search(request):
    """Enregistre une recherche d'adresse dans la base de données"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Méthode non autorisée'}, status=405)
    
    try:
        data = json.loads(request.body)
        
        # Valider les données essentielles
        if not data.get('query') or not data.get('latitude') or not data.get('longitude'):
            return JsonResponse({
                'success': False, 
                'error': 'Données incomplètes'
            }, status=400)
        
        # Créer et sauvegarder l'objet
        address_search = AddressSearch(
            query=data.get('query', ''),
            label=data.get('label', ''),
            score=data.get('score'),
            id_address=data.get('id_address', ''),
            citycode=data.get('citycode', ''),
            postcode=data.get('postcode', ''),
            city=data.get('city', ''),
            housenumber=data.get('housenumber', ''),
            street=data.get('street', ''),
            context=data.get('context', ''),
            latitude=data.get('latitude', 0),
            longitude=data.get('longitude', 0),
            x=data.get('x'),
            y=data.get('y'),
            type=data.get('type', ''),
            importance=data.get('importance')
        )
        address_search.save()
        
        logger.info(f"Recherche d'adresse enregistrée: {data.get('query')}")
        return JsonResponse({'success': True, 'id': address_search.id})
    
    except json.JSONDecodeError:
        logger.error("Erreur de décodage JSON")
        return JsonResponse({'success': False, 'error': 'Format JSON invalide'}, status=400)
    except Exception as e:
        logger.error(f"Erreur lors de l'enregistrement de la recherche: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

def search_address_view(request):
    return redirect('cartography:map')