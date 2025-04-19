import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
    static targets = ["container"]
    static values = {
        latitude: Number,
        longitude: Number,
        zoom: Number
    }

    connect() {
        const latitude = this.hasLatitudeValue ? this.latitudeValue : 48.856614
        const longitude = this.hasLongitudeValue ? this.longitudeValue : 2.3522219
        const zoom = this.hasZoomValue ? this.zoomValue : 13

        this.map = L.map(this.containerTarget).setView([latitude, longitude], zoom)

        L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
            subdomains: 'abcd',
            maxZoom: 20
        }).addTo(this.map)

        setTimeout(() => {
            this.map.invalidateSize()
        }, 0)
    }

    disconnect() {
        if (this.map) {
            this.map.remove()
            this.map = undefined
        }
    }
}