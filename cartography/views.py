from django.shortcuts import render


def map_view(request):
    facility_types = [
        {'value': '', 'label': 'Tous les établissements', 'emoji': ''},
        {'value': 'hospital', 'label': 'Hôpitaux', 'emoji': '🔴'},
        {'value': 'pharmacy', 'label': 'Pharmacies', 'emoji': '🟢'},
        {'value': 'doctors', 'label': 'Médecins', 'emoji': '🔵'},
        {'value': 'clinic', 'label': 'Cliniques', 'emoji': '🟠'},
    ]
    return render(request, 'cartography/map.html', {
        'facility_types': facility_types
    })