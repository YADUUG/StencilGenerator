import os
import cv2
import numpy as np
from flask import Flask, render_template, request, redirect, jsonify, session

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.secret_key = 'your_secret_key'  # Set your secret key for session management

# Ensure the uploads and static folders exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
if not os.path.exists('static'):
    os.makedirs('static')

# Function to create stencil effect based on threshold and sharpness
def create_stencil(image_path, threshold=128, sharpness=1.0):
    # Load the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Apply Gaussian blur for sharpness control
    # A higher sharpness value will reduce the blur (i.e., more detail)
    blur_size = int(sharpness * 2) + 1  # GaussianBlur kernel size must be an odd number
    smooth_image = cv2.GaussianBlur(image, (blur_size, blur_size), 0)

    # Apply binary threshold: white background, black object
    _, stencil = cv2.threshold(smooth_image, threshold, 255, cv2.THRESH_BINARY)

    # Save the output stencil image in the 'static' folder
    stencil_filename = 'edited_image-stencil.png'
    output_path = os.path.join('static', stencil_filename)

    # Debugging: print the path where the image is saved
    print(f"Saving stencil to: {output_path}")

    if cv2.imwrite(output_path, stencil):
        print(f"Image successfully saved to: {output_path}")
    else:
        print(f"Failed to save image to: {output_path}")

    return stencil_filename

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect('/')
    
    file = request.files['file']
    if file.filename == '':
        return redirect('/')
    
    # Save the uploaded file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Store the file path in session for real-time processing
    session['file_path'] = file_path

    # Return the page with the real-time controls
    return render_template('index.html', file_path=file.filename)

@app.route('/process', methods=['POST'])
def process_image():
    # Get the threshold and sharpness values from the AJAX request
    threshold = int(request.form.get('threshold'))
    sharpness = float(request.form.get('sharpness'))

    # Retrieve the file path from the session
    file_path = session.get('file_path')

    if not file_path:
        return jsonify({'error': 'File path not found in session'}), 400

    # Process the image based on the threshold and sharpness
    stencil_filename = create_stencil(file_path, threshold, sharpness)

    # Return the path to the processed image (in the 'static' folder)
    return jsonify({'stencil_image': stencil_filename})

if __name__ == '__main__':
    app.run(debug=True)
