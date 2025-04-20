import { Controller } from "@hotwired/stimulus";
import { fetchHealthFacilities } from "../services/open-data";

const DEFAULT_COORDINATES = {
    PARIS: {
        lat: 48.856614,
        lng: 2.3522219,
        zoom: 12
    }
};

const CLUSTER_OPTIONS = {
    showCoverageOnHover: false,
    maxClusterRadius: 80,
    spiderfyOnMaxZoom: true
};

export default class extends Controller {
    static targets = ["container", "typeFilter"];
    static values = {
        latitude: Number,
        longitude: Number,
        zoom: Number
    };

    connect() {
        console.log("🗺️ MapController connected");

        const latitude = this.hasLatitudeValue ? this.latitudeValue : DEFAULT_COORDINATES.PARIS.lat;
        const longitude = this.hasLongitudeValue ? this.longitudeValue : DEFAULT_COORDINATES.PARIS.lng;
        const zoom = this.hasZoomValue ? this.zoomValue : DEFAULT_COORDINATES.PARIS.zoom;

        this.map = L.map(this.containerTarget).setView([latitude, longitude], zoom);

        L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
            subdomains: 'abcd',
            maxZoom: 20
        }).addTo(this.map);

        L.control.scale({ imperial: false }).addTo(this.map);

        setTimeout(() => {
            this.map.invalidateSize();
        }, 0);

        this.mainClusterGroup = null;
        this.markersByType = {};

        this.loadFacilities();
    }

    disconnect() {
        if (this.map) {
            this.map.remove();
            this.map = undefined;
        }
    }

    centerMapOnCoordinates(latitude, longitude, zoom = 16) {
        if (this.map) {
            this.map.setView([latitude, longitude], zoom);
        }
    }

    addAddressMarker(latitude, longitude, label) {
        if (this.addressMarker) {
            this.map.removeLayer(this.addressMarker);
        }

        // Markerr pour l'adresse recherchée (sans popup atm)
        const addressIcon = L.divIcon({
            html: `<div style="background-color: #3b82f6; width: 14px; height: 14px; border-radius: 50%; border: 2px solid white;"></div>`,
            className: 'custom-div-icon',
            iconSize: [14, 14],
            iconAnchor: [7, 7]
        });

        this.addressMarker = L.marker([latitude, longitude], { icon: addressIcon })
            .addTo(this.map);
    }

    async loadFacilities(type = null) {
        try {
            const facilities = await fetchHealthFacilities(type);
            this.displayFacilities(facilities);
        } catch (error) {
            console.error("Erreur lors du chargement des établissements:", error);
        }
    }

    displayFacilities(facilities) {
        this.clearMarkers();

        // Filtrer les établissements avec des coordonnées valides (revoir ça car c'est pas super propre et que je skip certains etablissements)
        const validFacilities = facilities.filter(f =>
            f.latitude && f.longitude &&
            !isNaN(f.latitude) && !isNaN(f.longitude)
        );

        if (validFacilities.length === 0) {
            console.warn("Aucun établissement avec des coordonnées valides n'a été trouvé.");
            return;
        }

        const createDivIcon = (color) => L.divIcon({
            html: `<div style="background-color: ${color}; width: 12px; height: 12px; border-radius: 50%; border: 2px solid white;"></div>`,
            className: 'custom-div-icon',
            iconSize: [12, 12],
            iconAnchor: [6, 6]
        });

        const icons = {
            hospital: createDivIcon('red'),
            pharmacy: createDivIcon('green'),
            doctors: createDivIcon('blue'),
            clinic: createDivIcon('orange'),
            default: createDivIcon('gray')
        };

        // Créer un groupe de clusters
        const mainClusterGroup = L.markerClusterGroup(CLUSTER_OPTIONS);
        this.markersByType = {};

        validFacilities.forEach(facility => {
            const icon = icons[facility.type] || icons.default;

            const marker = L.marker([facility.latitude, facility.longitude], { icon: icon })
                .bindPopup(this.createPopupContent(facility));

            if (!this.markersByType[facility.type]) {
                this.markersByType[facility.type] = [];
            }
            this.markersByType[facility.type].push(marker);
            mainClusterGroup.addLayer(marker);
        });
        this.map.addLayer(mainClusterGroup);
        this.mainClusterGroup = mainClusterGroup;
    }

    createPopupContent(facility) {
        return `
        <div class="p-3 max-w-sm">
            <h3 class="text-lg font-bold text-teal-700 border-b border-gray-200 pb-2 mb-2">${facility.name}</h3>
            
            <div class="flex items-center mb-2">
                <span class="inline-block px-2 py-1 text-xs font-semibold bg-teal-100 text-teal-800 rounded-full">${facility.type}</span>
                ${facility.wheelchair ? `<span class="ml-2 inline-block px-2 py-1 text-xs font-semibold bg-blue-100 text-blue-800 rounded-full">♿ Accessible</span>` : ''}
            </div>
            
            <div class="space-y-1 text-sm text-gray-700">
                ${facility.city ? `
                <div class="flex items-start">
                    <svg class="h-4 w-4 text-gray-500 mt-0.5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                    </svg>
                    <span>${facility.city}</span>
                </div>
                ` : ''}
                    
                ${facility.phone ? `
                <div class="flex items-start">
                    <svg class="h-4 w-4 text-gray-500 mt-0.5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path>
                    </svg>
                    <span><a href="tel:${facility.phone}" class="text-teal-600 hover:underline">${facility.phone}</a></span>
                    </div>
                ` : ''}
                ${facility.opening_hours ? `
                    <div class="flex items-start">
                    <svg class="h-4 w-4 text-gray-500 mt-0.5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    <span>${facility.opening_hours}</span>
                </div>
                ` : ''}
            </div>
            </div>
        `;
    }

    clearMarkers() {
        if (this.mainClusterGroup) {
            this.map.removeLayer(this.mainClusterGroup);
        }
        this.mainClusterGroup = null;
        this.markersByType = {};
    }

    // Filtrage des types d'établissements
    filterFacilities(event) {
        const selectedType = event.currentTarget.value;
        if (this.markersByType && Object.keys(this.markersByType).length > 0) {
            if (this.mainClusterGroup) {
                this.map.removeLayer(this.mainClusterGroup);
            }

            const mainClusterGroup = L.markerClusterGroup(CLUSTER_OPTIONS);

            if (selectedType) {
                const markersOfType = this.markersByType[selectedType] || [];
                markersOfType.forEach(marker => {
                    mainClusterGroup.addLayer(marker);
                });
            } else {
                Object.values(this.markersByType).flat().forEach(marker => {
                    mainClusterGroup.addLayer(marker);
                });
            }
            this.map.addLayer(mainClusterGroup);
            this.mainClusterGroup = mainClusterGroup;
        } else {
            this.loadFacilities(selectedType);
        }
    }

    // Fonction pour reset les filtres sur le template
    resetFilters() {
        this.typeFilterTargets.forEach(radio => {
            radio.checked = radio.value === '';
        });

        if (this.markersByType && Object.keys(this.markersByType).length > 0) {
            if (this.mainClusterGroup) {
                this.map.removeLayer(this.mainClusterGroup);
            }
            const mainClusterGroup = L.markerClusterGroup(CLUSTER_OPTIONS);

            Object.values(this.markersByType).flat().forEach(marker => {
                mainClusterGroup.addLayer(marker);
            });

            this.map.addLayer(mainClusterGroup);
            this.mainClusterGroup = mainClusterGroup;
        } else {
            this.loadFacilities();
        }
    }
}