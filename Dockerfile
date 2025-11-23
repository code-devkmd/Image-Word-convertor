# Start from a Python base image that supports apt-get
FROM python:3.11-slim

# Install Tesseract OCR and other necessary libraries
# This is the ONLY way to guarantee Tesseract installation on Render
RUN apt-get update && \
    apt-get install -y tesseract-ocr libtesseract-dev && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /usr/src/app

# Copy the requirements file and install Python dependencies (including pytesseract and gunicorn)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Command to run the application using Gunicorn (app:app is correct for your project)
CMD ["gunicorn", "app:app"]