from django.db import models


class HealthFacilityType(models.Model):
    name = models.CharField(max_length=100)  
    icon = models.CharField(max_length=100, blank=True)
    display_order = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

class HealthFacility(models.Model):
    name = models.CharField(max_length=255)
    facility_type = models.ForeignKey(HealthFacilityType, on_delete=models.CASCADE, related_name='facilities')  
    is_active = models.BooleanField(default=True)
    
    # Accessibilité
    wheelchair = models.CharField(max_length=10, blank=True, null=True) 
    
    # Contact
    phone = models.CharField(max_length=20, blank=True, null=True) 
    opening_hours = models.TextField(blank=True, null=True)
    
    # Localisation administrative
    city = models.CharField(max_length=100, blank=True, null=True) 
    department = models.CharField(max_length=100, blank=True, null=True) 
    
    # Coords géographiques
    latitude = models.FloatField()  
    longitude = models.FloatField() 

    external_id = models.CharField(max_length=100, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.facility_type})"
    
    class Meta:
        indexes = [
            models.Index(fields=['facility_type']),
            models.Index(fields=['city']),
            models.Index(fields=['department']),
            models.Index(fields=['is_active']),
            models.Index(fields=['wheelchair']),
        ]

# Ici pour la barre de recherche d'adresse (API Adresse)
class AddressSearch(models.Model):
    query = models.CharField(max_length=255) 
    
    # Résultat
    label = models.CharField(max_length=255)
    score = models.FloatField(null=True)  
    
    id_address = models.CharField(max_length=50, blank=True, null=True)
    citycode = models.CharField(max_length=10, blank=True, null=True)
    postcode = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    
    # Détails de l'adresse
    housenumber = models.CharField(max_length=10, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    context = models.CharField(max_length=255, blank=True, null=True)
    
    # CoordS
    latitude = models.FloatField()
    longitude = models.FloatField()
    x = models.FloatField(null=True) 
    y = models.FloatField(null=True) 

    type = models.CharField(max_length=50, blank=True, null=True)
    importance = models.FloatField(null=True)
    

    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.label
    
    class Meta:
        indexes = [
            models.Index(fields=['query']),
            models.Index(fields=['city']),
            models.Index(fields=['postcode']),
            models.Index(fields=['created_at']),
        ]
        verbose_name = "Recherche d'adresse"
        verbose_name_plural = "Recherches d'adresses"