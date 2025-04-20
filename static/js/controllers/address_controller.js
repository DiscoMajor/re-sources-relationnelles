import { Controller } from "@hotwired/stimulus";
import TomSelect from "tom-select";
import 'tom-select/dist/css/tom-select.min.css';
import { searchAddress } from "../services/address-api";

export default class extends Controller {
    static targets = ["input", "form"];

    connect() {
        console.log("📍 AddressController connected");
        this.initTomSelect();

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

    disconnect() {
        if (this.tomSelect) {
            this.tomSelect.destroy();
        }
    }

    initTomSelect() {
        // Configuration de TomSelect le bon vieux TomSelect
        this.tomSelect = new TomSelect(this.inputTarget, {
            valueField: 'coordinates',
            labelField: 'label',
            searchField: 'label',
            create: false,
            persist: false,
            render: {
                option: function (item, escape) {
                    return `<div class="py-2 px-3 border-b border-gray-100">
                        <div class="font-medium">${escape(item.label)}</div>
                        <div class="text-xs text-gray-500">
                            ${item.type ? `${escape(item.type)}` : ''}
                            ${item.city ? `- ${escape(item.city)}` : ''}
                            ${item.postcode ? escape(item.postcode) : ''}
                        </div>
                    </div>`;
                },
                item: function (item, escape) {
                    return `<div>${escape(item.label)}</div>`;
                },
                no_results: function () {
                    return `<div class="py-2 px-3 text-gray-500">Aucun résultat trouvé</div>`;
                },
                not_loading: function () {
                    return `<div class="py-2 px-3 text-gray-500">Saisissez une adresse...</div>`;
                }
            },
            onItemAdd: function () {
                this.setTextboxValue('');
                this.refreshOptions();
            },
            load: (query, callback) => {
                if (!query.length || query.length < 3) return callback();
                searchAddress(query)
                    .then(result => {
                        if (!result.features || !result.features.length) {
                            return callback();
                        }
                        const options = result.features.map(feature => {
                            const coords = feature.geometry.coordinates;
                            const props = feature.properties;
                            return {
                                label: props.label,
                                type: props.type,
                                city: props.city,
                                postcode: props.postcode,
                                coordinates: [coords[1], coords[0]],
                                originalFeature: feature
                            };
                        });
                        callback(options);
                    })
                    .catch(error => {
                        console.error("Erreur lors de la recherche d'adresse:", error);
                        callback();
                    });
            },
            onChange: (value) => {
                if (!value) return;
                const selectedItem = this.tomSelect.options[value];
                if (selectedItem) {
                    if (this.mapController) {
                        const [latitude, longitude] = selectedItem.coordinates;
                        this.mapController.centerMapOnCoordinates(latitude, longitude);
                        this.mapController.addAddressMarker(latitude, longitude, selectedItem.label);
                    }
                    if (selectedItem.originalFeature) {
                        this.saveSearch(selectedItem.originalFeature);
                    }
                    this.tomSelect.clear(true);
                }
            }
        });
    }

    saveSearch(feature) {
        if (!feature) return;

        const props = feature.properties;
        const coords = feature.geometry.coordinates;

        fetch('/cartography/save-address-search/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCsrfToken()
            },
            body: JSON.stringify({
                query: props.label,
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