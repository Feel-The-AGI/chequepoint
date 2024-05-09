import cv2
import sys
import pytesseract
from PIL import Image
import requests
import json
import numpy as np

# Functions for image capture and loading
def capture_image_from_camera():
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if not ret:
        raise Exception("Failed to capture image from camera.")
    cam.release()
    return frame

def load_image_from_file(file_path):
    image = cv2.imread(file_path, cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError("Failed to load image from file.")
    return image

# Function to preprocess image for better OCR accuracy
def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return thresh

# Function for dynamically detecting and extracting text fields
def extract_features(image):
    preprocessed_image = preprocess_image(image)
    data = {}
    # Customize field detection and OCR settings based on expected cheque layout
    data['Account Number'] = pytesseract.image_to_string(preprocessed_image, config='--psm 7', lang='eng')
    data['Amount'] = pytesseract.image_to_string(preprocessed_image, config='--psm 7', lang='eng')
    data['Date'] = pytesseract.image_to_string(preprocessed_image, config='--psm 7', lang='eng')
    return data

# Function to upload data to the bank's API
def upload_data(api_url, data):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(api_url, headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        raise Exception("Failed to upload data to the bank's API.")
    return response

# Main driver function
def main():
    try:
        if len(sys.argv) > 1:
            file_path = sys.argv[1]
            image = load_image_from_file(file_path)
        else:
            image = capture_image_from_camera()

        extracted_data = extract_features(image)
        print("Extracted Data:", json.dumps(extracted_data, indent=2))

        api_url = "http://example.com/api/upload"  # Placeholder API URL
        response = upload_data(api_url, extracted_data)
        print("Upload Successful:", response.text)

    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    main()
