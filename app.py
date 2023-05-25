from flask import Flask, render_template, request, redirect, url_for
from flask_gzip import Gzip

from services import get_images_data_to_table, save_image

app = Flask(__name__)
gzip = Gzip(app)


@app.route('/')
async def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
async def upload():
    # Check if a file was sent
    if 'image' not in request.files:
        return 'No image selected'

    # Get the image in the application
    image = request.files['image']
    # Verify that a valid file is selected
    if image.filename == '':
        return 'No image selected'

    save_image('static/img', image)
    # Successful response
    return redirect(url_for('gallery'))


@app.route('/gallery')
async def gallery():
    return render_template('images.html', images=get_images_data_to_table('static/img'))


if __name__ == '__main__':
    app.run()
