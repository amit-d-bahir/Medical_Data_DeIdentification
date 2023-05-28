import re
from datetime import datetime

from data_extractor import data_extractor
from image_deidentifier import image_deidentifier
from pdf_deidentifier import pdf_deidentifier


def deidentification(input_string, input_files, flag):
    deidentified_string = data_extractor(input_string)
    deidentified_list = deidentified_string.splitlines()
    if flag == "streamlit":
        deidentified_files = _deidentify_files_streamlit(input_files)
    else:
        deidentified_files = _deidentify_files_api(input_files)

    deidentified_data = {}
    if _contains_only_periods(deidentified_list[0]):
        deidentified_data["description"] = ""
    else:
        deidentified_data["description"] = deidentified_list[0]

    if _contains_only_periods(deidentified_list[1]):
        deidentified_data["medicines"] = ""
    else:
        deidentified_data["medicines"] = deidentified_list[1]

    if _contains_only_periods(deidentified_list[2]):
        deidentified_data["injections"] = ""
    else:
        deidentified_data["injections"] = deidentified_list[2]

    if _contains_only_periods(deidentified_list[3]):
        deidentified_data["vitals"] = ""
    else:
        deidentified_data["vitals"] = deidentified_list[3]

    deidentified_data["files"] = deidentified_files
    return deidentified_data


def _deidentify_files_streamlit(input_files):
    deidentified_files = []
    for file in input_files:
        if file.type in ["image/png", "image/jpg", "image/jpeg"]:
            deid_img_path = image_deidentifier(file.name)
            deidentified_files.append(deid_img_path)
        elif file.type == "application/pdf":
            deid_pdf_path = pdf_deidentifier(file.name)
            deidentified_files.append(deid_pdf_path)
        elif file.type == "text/plain":
            bytes_data = file.read()
            text_string = bytes_data.decode('utf-8')
            processed_string = data_extractor(text_string)
            now = datetime.now()
            deid_text_path = "/Users/amitbahir/Hackathon/Medical_Data_DeIdentification/results/" + "deidentified_" \
                             + now.strftime("%d-%m-%Y %H:%M:%S:%f") + ".txt"
            with open(deid_text_path, "a") as f:
                f.write(processed_string)
            deidentified_files.append(deid_text_path)
    return deidentified_files


def _deidentify_files_api(input_files):
    deidentified_files = []
    for file in input_files:
        identifier = file[-3:]
        if identifier in ["png", "jpg", "jpeg"]:
            deid_img_path = image_deidentifier(file)
            deidentified_files.append(deid_img_path)
        elif identifier == "pdf":
            deid_pdf_path = pdf_deidentifier(file)
            deidentified_files.append(deid_pdf_path)
        elif identifier == "txt":
            with open(file, "r") as f:
                input_string = f.read()
            processed_string = data_extractor(input_string)
            now = datetime.now()
            deid_text_path = "../results/" + "deidentified_" + now.strftime("%d-%m-%Y %H:%M:%S:%f") + ".txt"
            with open(deid_text_path, "a") as f:
                f.write(processed_string)
            deidentified_files.append(deid_text_path)
    return deidentified_files


def _contains_only_periods(input_string):
    contains_only_periods = re.match(r"\.*$", input_string) is not None
    return contains_only_periods
