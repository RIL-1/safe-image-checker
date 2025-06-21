from flask import Flask, request, jsonify
from nudenet import Classifier
import os

app = Flask(__name__)
classifier = Classifier()

@app.route('/check-paths', methods=['POST'])
def check_paths():
    data = request.get_json()

    if not data or 'paths' not in data:
        return jsonify({'error': 'No image paths provided'}), 400

    image_paths = data['paths']
    if not isinstance(image_paths, list):
        return jsonify({'error': 'paths must be a list'}), 400

    results = {}

    for path in image_paths:
        path = '/data/images/' + path
        if not os.path.isfile(path):
            results[path] = {'error': 'File not found'}
            continue

        try:
            result = classifier.classify(path)
            results[path] = result.get(path, {})
        except Exception as e:
            results[path] = {'error': str(e)}

    return jsonify(results)
