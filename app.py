from flask import Flask, request, render_template
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import os
from werkzeug.utils import secure_filename
import tempfile # NEW: Import tempfile

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

app = Flask(__name__)

# NOTE: UPLOAD_FOLDER configuration is no longer strictly necessary for temporary files, 
# but we'll keep the logic clean.
# os.makedirs(UPLOAD_FOLDER, exist_ok=True) # REMOVE THIS LINE for safety

@app.route('/', methods=['GET'])
def index():
    # Ensure static files are referenced correctly in index.html
    return render_template('index.html', text=None)

@app.route('/upload', methods=['POST'])
def upload():
    # ... (file validation remains the same) ...

    file = request.files['image']
    if file.filename == '':
        return ("No file selected.", 400)

    # 1. Use a temporary file for storage
    # This creates a temporary file and returns a handle to it.
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    filepath = temp_file.name # Get the secure path
    temp_file.close() # Close the handle so PIL/Pytesseract can access the file

    try:
        # 2. Save the uploaded file content to the secure temporary path
        file.save(filepath)

        # 3. Image Processing & OCR (Your original logic)
        image = Image.open(filepath)
        image = image.convert('L')
        image = ImageEnhance.Contrast(image).enhance(2.0)
        image = image.filter(ImageFilter.GaussianBlur(radius=1))        
        text = pytesseract.image_to_string(image, config='--oem 3 --psm 6')

        # 4. Cleanup the temporary file
        os.remove(filepath)
        
        # 5. Return result
        return text, 200, {'Content-Type': 'text/plain; charset=utf-8'}
        
    except Exception as e:
        # Ensure cleanup even on error
        if os.path.exists(filepath):
             os.remove(filepath)
        
        # Log the error (will appear in Render logs)
        print(f"Error processing image: {e}") 
        return (f"Error processing image. Check server logs for details.", 500)

if __name__ == '__main__':
    # When running locally, Flask development server is fine
    app.run(debug=True)