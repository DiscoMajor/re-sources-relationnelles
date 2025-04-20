// static/js/controllers/address_controller.js
import { Controller } from "@hotwired/stimulus";
import { searchAddress } from "../services/address-api";

export default class extends Controller {
    static targets = ["input", "form", "results"];
    
    connect() {
        console.log("📍 AddressController connected");
        
        setTimeout(() => {
            const mapElement = document.querySelector("[data-controller='map']");
            if (mapElement) {
                this.mapController = this.application.getControllerForElementAndIdentifier(
                    mapElement,
                    "map"
                );
            } else {
                console.error("No map element found");
            }
        }, 100);
    }
    
    handleKeyDown(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            this.search();
        }
    }
    
    async search(event) {
        if (event) event.preventDefault();
        
        const query = this.inputTarget.value.trim();
        if (!query) return;
        
        try {
            const result = await searchAddress(query);
            this.saveSearch(result);
            
            if (result.features && result.features.length > 0) {
                const firstResult = result.features[0];
                const coordinates = firstResult.geometry.coordinates;
                
                const longitude = coordinates[0];
                const latitude = coordinates[1];
                
                if (this.mapController) {
                    this.mapController.centerMapOnCoordinates(latitude, longitude);
                    // Juste ajouter un marqueur sans popup
                    this.mapController.addAddressMarker(latitude, longitude);
                }
            }
        } catch (error) {
            console.error("Erreur lors de la recherche d'adresse:", error);
        }
    }
    
    saveSearch(result) {
        if (!result || !result.features || result.features.length === 0) return;
    
        const feature = result.features[0];
        const props = feature.properties;
        const coords = feature.geometry.coordinates;
        
        fetch('/cartography/save-address-search/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCsrfToken()
            },
            body: JSON.stringify({
                query: this.inputTarget.value,
                label: props.label,
                score: props.score,
                id_address: props.id,
                citycode: props.citycode,
                postcode: props.postcode,
                city: props.city,
                housenumber: props.housenumber,
                street: props.street,
                context: props.context,
                latitude: coords[1],
                longitude: coords[0],
                x: props.x,
                y: props.y,
                type: props.type,
                importance: props.importance
            })
        }).catch(error => {
            console.error("Erreur lors de l'enregistrement de la recherche:", error);
        });
    }
    
    getCsrfToken() {
        return this.formTarget.querySelector('input[name="csrfmiddlewaretoken"]').value;
    }
}