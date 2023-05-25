import requests
from PIL import Image
from PIL.ExifTags import TAGS


def transform_degrees_to_decimal(coordinates):
    degrees = coordinates[0]
    minutes = coordinates[1]
    seconds = coordinates[2]

    decimal_coordinates = degrees + (minutes / 60.0) + (seconds / 3600.0)

    return decimal_coordinates


def get_metadata_from_image(path):
    img = Image.open(path)
    metadata_data = img._getexif()
    metadata = {}

    if metadata_data is not None:
        for tag, value in metadata_data.items():
            tag_name = TAGS.get(tag, tag)
            metadata[tag_name] = value

    return metadata


def get_location_zone(metadata):
    location = 'Location unknown'
    if "GPSInfo" in metadata:
        gps_info = metadata["GPSInfo"]

        latitude_ref = gps_info.get(1)
        latitude = gps_info.get(2)
        longitude_ref = gps_info.get(3)
        longitude = gps_info.get(4)

        if latitude and longitude and latitude_ref and longitude_ref:
            decimal_latitude = transform_degrees_to_decimal(latitude)
            decimal_longitude = transform_degrees_to_decimal(longitude)

            if latitude_ref == 'S':
                decimal_latitude = -decimal_latitude
            if longitude_ref == 'W':
                decimal_longitude = -decimal_longitude

            response = requests.get(f"http://api.geonames.org/findNearbyPlaceNameJSON?lat={decimal_latitude}" \
                  f"&lng={decimal_longitude}&username=jorge.saenz")
            data = response.json()

            if "geonames" in data and data["geonames"]:
                location = data["geonames"][0]["name"]

            return [location, get_google_maps_location(decimal_latitude, decimal_longitude)]

    return [location]


def get_google_maps_location(decimal_latitude, decimal_longitude):
    return f"https://www.google.com/maps/search/?api=1&query={decimal_latitude},{decimal_longitude}"


def get_date_hour(metadata):
    if 'DateTime' in metadata or 'DateTimeOriginal' in metadata:
        # Get values in metadata tag
        datetime = str(metadata['DateTime']).split(' ') if 'DateTime' in metadata else \
            str(metadata['DateTimeOriginal']).split(' ')

        # Get date and format it
        date = '/'.join(datetime[0].split(':')[::-1])
        hour = datetime[1]

        return [date, hour]

    return ['Unknown']
