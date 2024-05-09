import cv2
import sys
import pytesseract
from PIL import Image
import requests
import json

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

# Function for extracting text using OCR
def extract_text(image):
    return pytesseract.image_to_string(image)

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
        
        extracted_text = extract_text(Image.fromarray(image))
        print("Extracted Text:", extracted_text)

        api_url = "http://jason.com/api/upload"  # Placeholder API URL
        data = {"extracted_data": extracted_text}
        response = upload_data(api_url, data)
        print("Upload Successful:", response.text)

    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    main()
