from flask import Flask, request, jsonify
import textract

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'pdf'}

@app.route('/upload', methods=['POST'])
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

@app.route('/pdf_contents', methods=['GET'])
def get_pdf_contents():
    # Read the PDF file and extract its contents
    text = textract.process('file.pdf').decode('utf-8')

    # Return the contents in JSON format
    return jsonify({'contents': text}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
