from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'dcm'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')

@app.route('/analyze_ct_scan', methods=['POST'])
def analyze_ct_scan():
    if 'ct_scan' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['ct_scan']
    name = request.form.get('name')
    age = request.form.get('age')
    sex = request.form.get('sex')

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # --- STEP 1: Load and Preprocess the CT Scan Image ---
        # ... (Your image loading and preprocessing code) ...
        processed_image = None # Placeholder

        if processed_image is None:
            return jsonify({'error': 'Failed to load or preprocess the image.'}), 500

        # --- STEP 2 & 3: Tumor Detection and Analysis ---
        # ... (Your tumor detection and analysis logic) ...
        tumor_detected = False
        tumor_size = None
        potential_tumor_type = None

        if processed_image is not None:
            tumor_detected = True
            tumor_size = "Approximately 1.5 cm (Placeholder)"
            potential_tumor_type = "Potentially Glioma (Placeholder)"

        return jsonify({
            'tumor_detected': tumor_detected,
            'tumor_size': tumor_size,
            'potential_tumor_type': potential_tumor_type,
            'message': 'Analysis performed (placeholder results).'
        })
    else:
        return jsonify({'error': 'Invalid file format. Allowed: png, jpg, jpeg, dcm'}), 400

if __name__ == '__main__':
    app.run(debug=True)