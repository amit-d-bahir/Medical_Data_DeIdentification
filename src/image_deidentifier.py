from datetime import datetime

import cv2
import numpy as np
import pytesseract
from PIL import Image

from data_extractor import data_extractor


def image_deidentifier(image_path):
    input_string = _img_ocr(image_path)
    processed_string = data_extractor(input_string)

    now = datetime.now()
    deid_img_path = "/Users/amitbahir/Hackathon/Medical_Data_DeIdentification/results/" + "deidentified_" + now.strftime("%d-%m-%Y_%H:%M:%S:%f") + ".txt"

    with open(deid_img_path, "a") as f:
        f.write(processed_string)

    return deid_img_path


def _img_ocr(image_path):
    # preprocessing it
    image = _img_preprocessing(image_path)

    return pytesseract.image_to_string(image, lang='eng')


def _img_preprocessing(image_path):
    # Getting the image from the URL provided
    image = Image.open(image_path)
    image_array = np.array(image)

    # Rescaling the image
    image = cv2.resize(image_array, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)

    # Converting it to grayscale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Now applying dilation and erosion to remove noise
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.erode(image, kernel, iterations=1)

    # Blurring to smooth out the edges
    image = cv2.GaussianBlur(image, (5, 5), 0)

    # Applying threshold to get only black and white image (Binarization)
    _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return image
