import cv2
import numpy as np
from PIL import Image, ImageEnhance

class parameters_processor:
    def remove_noise(self, image):
        """Remove noise by blurring"""
        noise_removed = cv2.GaussianBlur(image, (3, 3), 0)
        return noise_removed
    
    def enhance_sharpness(self, image):
        """Enhance sharpness of the image"""
        pil_image = Image.fromarray(image)
        enhancer = ImageEnhance.Sharpness(pil_image)
        enhanced_image = enhancer.enhance(2.6)
        return np.array(enhanced_image)

    def enhance_brightness(self, image):
        """Enhance brightness of the image"""
        pil_image = Image.fromarray(image)
        enhancer = ImageEnhance.Brightness(pil_image)
        enhanced_image = enhancer.enhance(2.2)
        return np.array(enhanced_image)
