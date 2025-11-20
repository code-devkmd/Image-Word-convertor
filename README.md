## 📄 Image to Text (OCR) Converter

A web application built using **Flask** and **Tesseract OCR** that allows users to upload an image and extract the embedded text. The upgraded version includes advanced image preprocessing using **OpenCV** for improved accuracy and a more user-friendly frontend experience.

## ✨ Features

- **File Upload & Drag-and-Drop:** Easily upload images via selection or drag-and-drop.

- **Image Preview:** See the uploaded image before conversion starts.

- **Advanced Preprocessing:** Uses Otsu's Binarization (via OpenCV) to enhance image quality for better OCR results.

- **Progress Tracking:** Shows real-time upload and processing progress via an XMLHttpRequest.

- **Text Extraction:** Utilizes pytesseract to convert the image content into editable text.

- **Copy & Clear:** Quick actions to copy the extracted text or reset the application.

## 🛠️ Technologies Used

**Backend (Python/Flask)**

  -  **Python 3**

  -  **Flask:** Web framework for routing and serving the application.

  -  **Pillow (PIL):** Basic image handling.

  -  **pytesseract:** Python wrapper for Tesseract OCR.

  -  **opencv-python (cv2):** Used for robust image preprocessing (Grayscale, Median Blur, Otsu's Binarization).

  -  **numpy:** Used by OpenCV for image array manipulation.

**Frontend (Web)**

  -  **HTML5 & CSS3:** Structure and styling.

  -  **JavaScript (ES6):** Handling file uploads, drag-and-drop, image preview, and AJAX (XMLHttpRequest) submission with progress tracking.

## 🚀 Setup and Installation

1. **Prerequisites**

You must have **Tesseract OCR** installed on your operating system, as pytesseract is just a wrapper for the command-line tool.

  -  **Tesseract OCR:** Download from GitHub or install via your system's package manager (e.g., sudo apt install tesseract-ocr on Debian/Ubuntu, brew install tesseract on macOS).

2. **Python Environment Setup**

  -  Clone the repository (if applicable) or navigate to the project directory.

  -  Create a virtual environment (recommended):

```bash
python -m venv venv
```

3. **Activate the virtual environment:**

  -  **Windows:** venv\Scripts\activate

  -  **macOS/Linux:** source venv/bin/activate

Install the required Python packages:

```bash
    pip install Flask pytesseract Pillow opencv-python numpy
```

4. **Running the Application**

  1.  Ensure the directory structure is correct:

```bash
    .
    ├── app.py
    └── static/
        ├── style.css
        └── script.js
    └── templates/
        └── index.html
    └── uploads/  # Created automatically
```

  2.  Run the Flask application:

```bash
    python app.py
```

  3.  Access the application in your web browser at: http://127.0.0.1:5000/

## 💡 How to Use

1.    Open the Application in your browser.

2.    Upload an Image: Drag and drop an image file (PNG, JPG, etc.) onto the dashed area, or click the area to open a file selection dialog.

3.    Preview: The selected image will appear below the upload box.

4.    Convert: Click the "Convert Image" button. The progress bar will indicate the upload and server-side processing time.

5.    View Results: The extracted text will appear in the dedicated text area.

6.    Actions: Use the "Copy Text" button to quickly copy the result to your clipboard or "Clear All" to reset the application for a new image.