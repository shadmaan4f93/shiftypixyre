import mapbox
from mapbox import Directions
from lambdas.config.config import MAPBOX_TOKEN


GEOCODER = mapbox.Geocoder(access_token=MAPBOX_TOKEN["mapbox_token"])


class Geolocation:
    """ The Geolocation class is use to provide mapbox services.

    Note: Geolocation class have static method you can direct call class method.
          Example: Geolocation.get_lat_lng("Address")

    Methods: get_lat_lng, get_address, distance. """

    @staticmethod
    def get_lat_lng(address):
        """ This function use to get lat, lng value from address.

        Args:
            address (string): Address as string Example: "Delhi, 110092, India".

        Returns:
            coordinates: (dict) The return value. """
        # Initialize return value.
        return_value = {
            "latitude": None,
            "longitude": None
        }
        try:
            # Call mapbox client to get address.
            response = GEOCODER.forward(address)
            # To check client called success.
            if response.status_code == 200:
                address_component = response.json()
                coordinates = address_component["features"][0]["geometry"]["coordinates"]
                return_value["longitude"] = coordinates[0]
                return_value["latitude"] = coordinates[1]
        except BaseException:
            return_value = return_value
        return return_value

    @staticmethod
    def get_address(location):
        """ This function use to get address from lat, lng value.

        Args:
        lat_lng (dict): latitude, longitude list Example: {"longitude": 18.167489, "latitude": 77.16467].

        Returns:
        string: (Formated address) The return value. """

        try:
            # Get revers of geocode object.
            latitude = location['latitude']
            longitude = location['longitude']
            response = GEOCODER.reverse(lon=longitude, lat=latitude)
            address_component = response.json()
            address = address_component["features"][0]["place_name"]
            return address
        except BaseException:
            return None

    @staticmethod
    def distance(source, destination, distance_in=None):
        """ This function use to get distance between two address.

        Args:
        source (string/list): Source address string/ lat, lng as list.
        destination (string/list): Destination address string/ lat, lng as list.
        distance_in(string): Type of distance. Example: meter, kelometer, miles.

        Returns:
        Float: Distance The return value. """
        # Initialize return value.
        return_value = 0
        try:
            origin = (source['longitude'], source['latitude'])
            destination = (destination['longitude'], destination['latitude'])
            # Call mapbox client to get direction services.
            response = Directions(MAPBOX_TOKEN["mapbox_token"]).directions([origin, destination])
            driving_routes = response.geojson()
            distances = driving_routes['features'][0]['properties']["distance"]
            if not distance_in:
                return_value = distances * 0.00062137
            elif distance_in == "kelometer":
                return_value = round(distances / 1000, 2)
        except BaseException:
            return_value = 0
        return return_value
