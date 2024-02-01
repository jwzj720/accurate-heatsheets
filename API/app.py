import os
from helpers import *
from flask import  Flask, request, session, jsonify
from flask_cors import cross_origin
from pdf_parser.pdf_parsing import extract_dict_from_heat_sheet
from flask import jsonify
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
# You need to create your own 'app_settings.py" file
app.config.from_object('app_settings')


@app.route('/upload', methods=['POST'])
@cross_origin()
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file and allowed_file(file.filename):
        # secure_filename returns a secure version of the filename
        filename = secure_filename(file.filename)
        uuid = generate_uuid()
        filename = add_uuid_to_filename(filename,uuid)
        # save file to upload folder
        file.save(os.path.join(app.config['UPLOAD_FOLDER']),filename)
        # save the filename in a session var for later access
        session['filename'] = filename
        
        return jsonify({'message': 'File uploaded successfully','uuid':uuid}), 200
    else:
        return jsonify({'error': 'Invalid file format'}), 400

@app.route('/pdf/', methods=['GET'])
def return_info():
    """
    Take in the filename
    extract json from pdf
    query database
    turn into panda dataframe
    return csv
    """
    if session['filename']:
        filename =os.path.join(app.config['UPLOAD_FOLDER'], session['filename']) 
    else:
        return jsonify({'error': 'No file uploaded'}), 400
    
    meet_info_from_pdf = extract_dict_from_heat_sheet(filename)
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)