import { Application } from "@hotwired/stimulus"
import MapController from "./controllers/map_controller"
import AddressController from './controllers/address_controller';

const application = Application.start()
application.register("map", MapController)
application.register('address', AddressController);