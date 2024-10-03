# Paddle OCR Truck License Plate Recognition System

Welcome to the **Paddle OCR Truck License Plate Recognition System**! This innovative project harnesses the power of PaddleOCR to accurately identify truck license plates from images stored in a designated folder.

## Key Features:
- **Image Processing:** The system enhances image quality through advanced techniques such as noise reduction and sharpening.
- **Plate Color Detection:** It intelligently extracts license plate numbers while determining their colors—either Yellow or White.
- **Flexible Configuration:** Customize your processing parameters effortlessly through the `parameters.py` file to tailor the recognition process to your specific requirements.
- **Automated Workflow:** Seamlessly processes images in real-time, archiving or removing processed files as needed to keep your directory organized.

## Recommended Approach
To enhance the accuracy of your license plate recognition, we recommend implementing a preliminary detection step using the **YOLO (You Only Look Once)** model. By integrating YOLO for license plate detection, you can significantly improve the success rate of recognizing plates before processing them with this OCR system.

## How to Get Started:
1. Set your input and archive paths.
2. Adjust the parameters in `parameters.py` as needed.
3. Run the script to start processing!

## Final Thoughts
With this robust system, you can extend the functionality and adapt it to various use cases in license plate recognition. Implementing YOLO as a detection mechanism can lead to more reliable results and improved project success.
