import os
from flask import  Flask, flash, request, redirect, url_for, session, jsonify
from pdf_parser.pdf_parsing import extract_json_from_heat_sheet
from flask import jsonify
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
# You need to create your own 'app_settings.py" file
app.config.from_object('app_settings')

def allowed_file(filename): 
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload/', methods=['POST','GET'])
def upload_file():
    print(os.getcwd())
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            session['filename'] = filename
            return redirect(url_for('upload_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
@app.route('/pdf/', methods=['GET'])
def return_info():
    filename =os.path.join(app.config['UPLOAD_FOLDER'], session['filename']) 
    if session['filename']:
        json_output = jsonify(extract_json_from_heat_sheet(filename))
        return json_output
    else:
        return "ERROR NO FILE"
        


    
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)