import os
from flask import Flask, render_template, request, jsonify
from flask_gzip import Gzip
from flask_cors import CORS

from services import get_images_data_to_table, save_image

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
gzip = Gzip(app)

FILE_NAMES = []


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
    return get_images_data_to_table('static/img', FILE_NAMES[len(FILE_NAMES) - 1])


@app.route("/charge")
def charge():
    FILE_NAMES = os.listdir("static/img")
    
    data = []
    for f in FILE_NAMES:
        data.append(get_images_data_to_table('static/img', f))
        
    print(data)
    
    return data


if __name__ == '__main__':
    app.run()
