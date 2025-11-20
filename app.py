from flask import Flask, request, render_template, redirect, url_for
import pytesseract
from PIL import Image
import os
from werkzeug.utils import secure_filename
import cv2 # New: for advanced image processing
import numpy as np # New: for advanced image processing

app = Flask(__name__)

# --- Configuration ---
UPLOAD_FOLDER = os.path.join(app.root_path, "uploads")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB limit

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image_for_ocr(filepath):
    """
    Advanced image preprocessing using OpenCV for better OCR results.
    1. Load image in grayscale.
    2. Apply a median blur to reduce noise.
    3. Apply Otsu's Binarization to separate text from background.
    """
    try:
        # Load image with OpenCV
        img_cv = cv2.imread(filepath)
        if img_cv is None:
            raise IOError("OpenCV could not read the image.")

        # Convert to grayscale
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

        # Apply a median blur to remove noise
        blur = cv2.medianBlur(gray, 3)

        # Apply Otsu's Binarization
        _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Save the preprocessed image temporarily for pytesseract
        temp_filepath = filepath + "_preprocessed.png"
        cv2.imwrite(temp_filepath, thresh)
        
        return temp_filepath
    except Exception as e:
        print(f"Preprocessing error: {e}")
        # Fallback: if OpenCV fails, return the original filepath
        return filepath


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', text=None)

@app.route('/upload', methods=['POST'])
def upload():
    # 1. File validation
    if 'image' not in request.files:
        return ("No file part in the request.", 400)

    file = request.files['image']
    if file.filename == '':
        return ("No file selected.", 400)
    
    if not allowed_file(file.filename):
        return ("Invalid file type. Only images are allowed.", 415)
        
    # 2. File saving
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    # 3. Image Processing & OCR
    preprocessed_path = None
    try:
        # Step a: Preprocess the image
        preprocessed_path = preprocess_image_for_ocr(filepath)
        
        # Step b: Perform OCR on the (potentially) preprocessed image
        # Using a higher page segmentation mode (e.g., --psm 3) is generally more robust
        image = Image.open(preprocessed_path)
        text = pytesseract.image_to_string(image, config='--oem 3 --psm 3')
        
        # 4. Cleanup (optional but good practice)
        os.remove(filepath)
        if preprocessed_path and preprocessed_path != filepath and os.path.exists(preprocessed_path):
             os.remove(preprocessed_path)
             
    except Exception as e:
        # Ensure cleanup on error
        if os.path.exists(filepath):
             os.remove(filepath)
        if preprocessed_path and os.path.exists(preprocessed_path):
             os.remove(preprocessed_path)
             
        # Log the error and return a generic message to the user
        print(f"Error processing image: {e}")
        return (f"Error during OCR processing. Check server logs.", 500)

    # 5. Success
    return text, 200, {'Content-Type': 'text/plain; charset=utf-8'}

if __name__ == '__main__':
    # NOTE: In a production environment, debug=True should be disabled
    app.run(debug=True)