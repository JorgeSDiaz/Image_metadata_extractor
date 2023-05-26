import os

from metadata import get_metadata_from_image, get_location_zone, get_date_hour


def save_image(path, image) -> str:
    name = (
        "".join(image.filename.split(" "))
        .replace("(", "")
        .replace(")", "")
        .replace("-", "")
    )
    # Save the image in the path
    image.save(path + "/" + name)
    return name


def get_images_data_to_table(path, name):
    # Get the list of files in the folder

    metadata = get_metadata_from_image(path + "/" + name)

    date_hour = get_date_hour(metadata)
    location = get_location_zone(metadata)

    return {
            "name": os.path.splitext(name)[0],
            "date": date_hour[0],   
            "hour": date_hour[1] if len(date_hour) > 1 else date_hour[0],
            "url": os.path.join(path, name),
            "location": location[0],
            "button": location[1] if len(location) > 1 else "",
        }
