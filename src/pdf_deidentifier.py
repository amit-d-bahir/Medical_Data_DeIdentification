import os
from datetime import datetime

import pytesseract
from PIL import Image
from pdf2image import convert_from_path

from data_extractor import data_extractor


def pdf_deidentifier(pdf_file_path):
    # pdf_file_path = url_to_pdf(url)
    txt_file_path = _pdf_ocr(pdf_file_path)

    with open(txt_file_path, "r") as f:
        input_string = f.read()

    processed_string = data_extractor(input_string)

    now = datetime.now()
    deid_pdf_path = "/Users/amitbahir/Hackathon/Medical_Data_DeIdentification/results/" + "deidentified_" + now.strftime(
        "%d-%m-%Y_%H:%M:%S:%f") + ".txt"

    with open(deid_pdf_path, "a") as f:
        f.write(processed_string)

    # Deleting temp file created for processing
    os.remove(txt_file_path)
    return deid_pdf_path


def _pdf_ocr(pdf_file_path):
    pages = convert_from_path(pdf_file_path, 500)

    # To store images of each page of PDF to image
    image_counter = 1
    now = datetime.now()
    for page in pages:
        filename = "/Users/amitbahir/Hackathon/Medical_Data_DeIdentification/results/page_" + now.strftime(
            "%d-%m-%Y_%H:%M:%S:%f_") + str(image_counter) + ".jpg"
        page.save(filename, 'JPEG')
        image_counter = image_counter + 1

    txt_file_path = "/Users/amitbahir/Hackathon/Medical_Data_DeIdentification/results/" + "to_be_deidentified" + now.strftime(
        "%d-%m-%Y_%H:%M:%S:%f") + ".txt"

    with open(txt_file_path, "a") as f:
        for i in range(1, image_counter):
            filename = "/Users/amitbahir/Hackathon/Medical_Data_DeIdentification/results/page_" + now.strftime(
                "%d-%m-%Y_%H:%M:%S:%f_") + str(i) + ".jpg"
            text = str((pytesseract.image_to_string(Image.open(filename))))
            text = text.replace('-\n', '')
            f.write(text)
            # Deleting temp file created for processing
            os.remove(filename)
    return txt_file_path
