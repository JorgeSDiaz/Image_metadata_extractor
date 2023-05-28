import os
from flask import Flask, render_template, request, jsonify
from flask_gzip import Gzip
from flask_cors import CORS

from services import get_images_data_to_table, save_image
from google_api_service import extract_images_from_drive_folder

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
gzip = Gzip(app)

FILE_NAMES = []
DATA = {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    # Check if a file was sent
    if 'image' not in request.files:
        return jsonify({'error': 'No image selected'}), 400

    # Get the image in the application
    image = request.files['image']
    # Verify that a valid file is selected
    if image.filename == '':
        return jsonify({'error': 'No image selected'}), 400
    
    name = save_image('static/img', image)
    if name in FILE_NAMES:
        return jsonify({'error': 'Already Exist'}), 400
    
    FILE_NAMES.append(name)
    print(FILE_NAMES)
    
    return "OK"


@app.route('/gallery')
def gallery():
    name = FILE_NAMES[len(FILE_NAMES) - 1]
    DATA[name] = get_images_data_to_table('static/img', name)
    return DATA.get(name)


@app.route("/charge")
def charge():
    extract_images_from_drive_folder('1exVAksxzJS4knfayDY176WEUYva9pBqS', 'static/img')
    FILE_NAMES = os.listdir("static/img")
        
    for f in FILE_NAMES:
        if f not in DATA.keys():
            DATA[f] = get_images_data_to_table('static/img', f)
        
    return [data for data in DATA.values()]


if __name__ == '__main__':
    app.run()
