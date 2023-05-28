import streamlit as st
from flask import Flask, request, jsonify
from flask_cors import CORS

from deidentifier import deidentification

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

app = Flask(__name__)
CORS(app)

st.title('Medical Data De-Identification')

description = st.text_input('DESCRIPTION', '')
medicines = st.text_input('MEDICINES', '')
bodyVitals = st.text_input('VITALS', '')
injections = st.text_input('INJECTIONS [if any]', '')

uploaded_files = st.file_uploader(
    label="LABORATORY / DIAGNOSTIC REPORTS",
    type=['png', 'jpg', 'jpeg', 'pdf', 'txt'],
    help="Lab tests and diagnostic procedures are tests used to check if a person's health is normal. For example, "
         "a lab can test a sample of your blood, urine or body tissue to see if something is wrong. A diagnostic "
         "test, like blood pressure testing, can show if you have low or high blood pressure.",
    accept_multiple_files=True)

if st.button('SUBMIT', use_container_width=True):
    input_string = description + ".\n" + medicines + ".\n" + injections + ".\n" + bodyVitals + ".\n"
    deidentified_data = deidentification(input_string, uploaded_files, "streamlit")

    st.header("Voila! We have De-Identified Your Data")

    if "description" in deidentified_data and deidentified_data["description"] != "":
        st.text_input('', 'DESCRIPTION', disabled=True)
        st.text(deidentified_data['description'])

    if "medicines" in deidentified_data and deidentified_data["medicines"] != "":
        st.text_input('', 'MEDICINES', disabled=True)
        st.text(deidentified_data['medicines'])

    if "vitals" in deidentified_data and deidentified_data["vitals"] != "":
        st.text_input('', 'VITALS', disabled=True)
        st.text(deidentified_data['vitals'])

    if "injections" in deidentified_data and deidentified_data["injections"] != "":
        st.text_input('', 'INJECTIONS', disabled=True)
        st.text(deidentified_data['injections'])

    if "files" in deidentified_data and deidentified_data["files"] != []:
        st.text_input('', 'LABORATORY / DIAGNOSTIC REPORTS', disabled=True)
        for file in deidentified_data["files"]:
            with open(file, "rb") as f:
                bytes_data = f.read()
            st.download_button("Download File", data=bytes_data, file_name="file.txt", mime="text/plain")
            st.text(bytes_data)


@app.route("/deidentification", methods=["POST"])  # Creating a decorator
def deidentification_endpoint():
    if request.method == 'POST':
        request_data = request.get_json()
        string = request_data['description'] + ".\n" + request_data['medicine'] + ".\n" + request_data[
            'injection'] + ".\n" + request_data['vitals'] + ".\n"
        deidentified_data_response = deidentification(string, request_data['files'], "api")
        return jsonify(deidentified_data_response)
    return jsonify({"message": "Didn't perform de_identification"})


@app.route("/status")
def status():
    return "We are Up & Running!"

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=9009)
