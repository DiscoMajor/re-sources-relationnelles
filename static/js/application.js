// static/js/application.js
import { Application } from "@hotwired/stimulus"
import MapController from "./controllers/map_controller"

const application = Application.start()
application.register("map", MapController)