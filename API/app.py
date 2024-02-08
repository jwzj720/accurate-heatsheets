import os
import traceback
from flask import  Flask, request, session, jsonify, redirect, url_for, send_file, make_response
from flask_cors import cross_origin, CORS
from flask import jsonify
from werkzeug.utils import secure_filename
from helpers import *

ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": ["https://accurate-heat-sheets.com"]
    }
})
# You need to create your own 'app_settings.py" file
app.config.from_object('app_settings')

@app.route('/upload', methods=['POST'])
@cross_origin() #specifies that resources like files can be shared across origins
def upload_pdf():
    if 'file' not in request.files:
        app.logger.error("Error, no file uploaded ")
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    
    if file.filename == '':
        app.logger.error("Error, no file selected ")
        return jsonify({'error': 'No file selected'}), 400

    if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
        # secure_filename returns a secure version of the filename
        filename = secure_filename(file.filename)
        uuid = generate_uuid()
        filename = add_uuid_to_filename(filename,uuid)
        # save file to upload folder
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        # save the filename in a session var for later access
        app.logger.info(f"File uploaded successfully. filename: {filename}")
        return jsonify({'message': 'File uploaded successfully','filename':filename}), 200
    else:
        app.logger.error("Error invalid file format")
        return jsonify({'error': 'Invalid file format'}), 400

@app.route('/pdf/<filename>', methods=['GET','POST'])
@cross_origin()
def return_info(filename):
    try: 
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        app.logger.info(f"File received: {filename}")
    except Exception as e :
        app.logger.error("Error finding file", exc_info=True)
        traceback.print_exc() # print stack trace to flask logs
        return jsonify({'error': 'No file uploaded', 'exception_type': str(e)}), 400
    
    try:
        meet_info_from_pdf = extract_dict_from_heat_sheet(file_path)
        app.logger.info(f"Meet info generated!")
    except Exception as e:
        app.logger.error("Error parsing pdf")
        traceback.print_exc()
        return jsonify({'error': 'could not parse PDF','exception_type':e}), 400
    
    try:
        csv_file,output_file_name = create_csv(filename,meet_info_from_pdf,download_folder=app.config['DOWNLOAD_FOLDER'])
        app.logger.info(f"CSV file created: {output_file_name}")
    except Exception as e:
        if e == FileNotFoundError:
            app.logger.error("File not found")
            return jsonify({'error': 'File not found.'}), 400
        else:
            app.logger.error("ERROR CREATING CSV FILE")
            traceback.print_exc()
            return jsonify({'error': 'Error creating csv.','exception_type':e}), 400

    
    response = make_response(send_file(output_file_name, download_name="results_new.csv"))
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Content-Type'] = 'text/csv'
    app.logger.info("Sucessfully sent csv to vue app")
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
