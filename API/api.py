from flask import Flask, request, jsonify, send_file
import textract
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf'} # ensures the file is actually a .pdf file
    # TODO: make sure that we check the file isn't too large, malicious, etc.

@app.route('/upload', methods=['POST'])
@cross_origin()
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file and allowed_file(file.filename):
        # Save the uploaded file to a location
        file.save('file.pdf')
        return jsonify({'message': 'File uploaded successfully'}), 200
    else:
        return jsonify({'error': 'Invalid file format'}), 400

@app.route('/download', methods=['GET'])
@cross_origin()
def send_pdf():
    try:
        return send_file('/home/wjones/CC/Capstone/tbd2/heat_sheets/BrianC.pdf', as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
