from datetime import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS

from deidentification.data_extractor import data_extractor
from deidentification.image_deidentifier import image_deidentifier
from deidentification.pdf_deidentifier import pdf_deidentifier

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

app = Flask(__name__)
CORS(app)


@app.route("/deidentification", methods=["POST"])  # Creating a decorator
def deidentification():
    if request.method == 'POST':
        request_data = request.get_json()
        string = request_data['description'] + ".\n" + request_data['medicine'] + ".\n" + request_data[
            'injection'] + ".\n" + request_data['labReport'] + ".\n"
        deidentified_string = data_extractor(string)
        deidentified_list = deidentified_string.splitlines()

        # Deidentifying files
        deidentified_files = []
        for file in request_data['files']:
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

        # Now deidentifying fields
        deidentified_data = {
            'description': deidentified_list[0],
            'medicine': deidentified_list[1],
            'injection': deidentified_list[2],
            'labReport': deidentified_list[3],
            'files': deidentified_files
        }
        return jsonify(deidentified_data)

    return jsonify({"message": "Didn't perform de_identification"})


@app.route("/status")
def status():
    return "We are Up & Running!"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9009)
