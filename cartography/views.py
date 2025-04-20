# Ajouter à views.py
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import AddressSearchForm
from .models import AddressSearch

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

@csrf_exempt  # uniquement pour des tests, utiliser csrf_protect en production !!!
def save_address_search(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
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
            
            return JsonResponse({'success': True, 'id': address_search.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

def search_address_view(request):
    """Vue pour gérer la soumission du formulaire de recherche d'adresse"""
    if request.method == 'GET':
        query = request.GET.get('address', '')
        if query:
            pass
    return redirect('cartography:map')