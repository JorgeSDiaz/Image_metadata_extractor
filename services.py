import os

from metadata import get_metadata_from_image, get_location_zone, get_date_hour


def save_image(path, image):
    # Save the image in the path
    image.save(path + '/' + image.filename)


def get_images_data_to_table(path):
    # Get the list of files in the folder
    file_names = os.listdir(path)

    # Filter image files only (.jpg, .jpeg, .png, .gif)
    image_files = [f for f in file_names if f.endswith(('.jpg', '.jpeg', '.png', '.gif'))]

    # Build the array with the data to be displayed in the table for each image.
    images = []
    for img in image_files:
        metadata = get_metadata_from_image(path + '/' + img)

        date_hour = get_date_hour(metadata)
        location = get_location_zone(metadata)

        images.append({'name': os.path.splitext(img)[0],
                       'date': date_hour[0],
                       'hour': date_hour[1] if len(date_hour) > 1 else date_hour[0],
                       'url': os.path.join(path, img),
                       'location': location[0],
                       'button': {
                           'disable': False if len(location) > 1 else True,
                           'url': location[1] if len(location) > 1 else ''
                       }
                       })

    return images
