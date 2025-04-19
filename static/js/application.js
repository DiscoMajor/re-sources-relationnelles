import { Application } from "@hotwired/stimulus"
import MapController from "./controllers/map_controller"

window.addEventListener('DOMContentLoaded', () => {
    const application = Application.start()
    application.register("map", MapController)
})