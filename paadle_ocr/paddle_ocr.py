import os
import shutil
import cv2
import numpy as np
import re
from paddleocr import PaddleOCR
import logging
import time
from parameters import parameters_processor

input_folder_path = r'C:\Users\ARoumpattana\Desktop\OCR\Data_Plate\processing\truck_d'
archive_path = r'your_archive_path'
archive_Switch = False # Set to True to save processed images to the archive

def replace_special_symbols(text):
    text = re.sub(r'[\{\|\}\[\]\/\\lJ]', '1', text)
    text = re.sub(r':', '-', text)
    text = re.sub(r'"', '-', text)
    text = re.sub(r'[.\s+]', '', text) 
    return text

def clean_text(text):
    text = re.sub(r'[^\w\s-]', '', text)
    text = text.strip()
    return text

def format_plate_number(plate_number):
    if len(plate_number) >= 6 and '-' not in plate_number:
        return plate_number[:2] + '-' + plate_number[2:]
    return plate_number

def detect_license_plate_color(hsv_image):
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)
    yellow_pixels = cv2.countNonZero(mask)
    total_pixels = hsv_image.shape[0] * hsv_image.shape[1]
    threshold = 0.1 * total_pixels
    if yellow_pixels > threshold:
        color = 'Yellow'
    else:
        color = 'White'
    return color

class OCRProcessor:
    def __init__(self):
        """Initialize PaddleOCR"""
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)

    def show_ocr_results(self):
        """Display OCR results"""
        plate_confidences = []

        if not self.result:
            print("\nNo OCR results")
            return

        for _, (text, score) in self.result:
            prob = round(score, 2)
            text = replace_special_symbols(text)
            text = clean_text(text)
            if re.match(r'^(?:\d{4}|\d{5}|\d{6}|\d{7}|\d{1,6}-\d{1,6}|\d{2}-)$', text):
                formatted_plate_number = format_plate_number(text)
                plate_confidences.append((formatted_plate_number, prob))

        # Select the registration number with the highest confidence value.
        if plate_confidences:
            highest_confidence_plate = max(plate_confidences, key=lambda x: x[1]) # Use the second-order (confidence) lambda function using max.
            cleaned_plate_numbers = highest_confidence_plate[0] # Keep the list number 1 (registration)

            # In the case of receiving multiple numbers and renewing the license plate code
            if len(cleaned_plate_numbers) < 7:
                sorted_confidences = sorted(plate_confidences, key=lambda x: x[1], reverse=True)
                if len(sorted_confidences) > 1: 
                    second_highest_confidence_plate = sorted_confidences[1]
                    if len(second_highest_confidence_plate[0]) == 4:
                        cleaned_plate_numbers = f"{cleaned_plate_numbers}{second_highest_confidence_plate[0]}"
                        cleaned_plate_numbers = format_plate_number(cleaned_plate_numbers)

            # Final Check
            if re.match(r'^\d{2}-\d{4}$|^\d{3}-\d{4}$', cleaned_plate_numbers):
                cleaned_plate_numbers
                color = detect_license_plate_color(self.hsv_image)
            else:
                cleaned_plate_numbers = "Some license plate data is missing"
                color = None
        else:
            cleaned_plate_numbers = "Unable to process license plate code."
            color = None

        print(f"\nPlate Number : {cleaned_plate_numbers} (confidence : {prob:.2f})")
        print(f'Color : {color}')

        self.color = color
        self.cleaned_plate_numbers = cleaned_plate_numbers
    
    def ocr_read(self, image_processor):
        """Read text from image"""
        self.result = self.ocr.ocr(image_processor, cls=True)[0]
        self.show_ocr_results()

    def process_images_in_folder(self, folder_path, archive_folder, move_to_archive=True):
        """Process all jpg images in the specified folder and optionally move processed files to archive."""
        while True:
            if os.path.exists(folder_path):
                files = [f for f in os.listdir(folder_path) if f.endswith('.jpg')]
                time.sleep(2)
                if files:
                    for filename in files:
                        image_path = os.path.join(folder_path, filename)
                        image = cv2.imread(image_path)
                        if image is not None:
                            self.hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                            rm_n = parameters.remove_noise(image)
                            es = parameters.enhance_sharpness(rm_n)
                            eb = parameters.enhance_brightness(es)
                            self.ocr_read(eb)
                            if move_to_archive:
                                archive_image_path = os.path.join(archive_folder, filename)
                                shutil.move(image_path, archive_image_path)
                            else:
                                os.remove(image_path)
                        else:
                            print(f"Image not found: {image_path}")
                    
                    print("\nWaiting for the next set of images...\n")
                else:
                    print("The folder is empty. Waiting for new .jpg images...")
                    time.sleep(2)
            else:
                print(f"The folder {folder_path} does not exist.")
                break

parameters = parameters_processor()
processor = OCRProcessor()
processor.process_images_in_folder(input_folder_path, archive_path, move_to_archive=archive_Switch)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
