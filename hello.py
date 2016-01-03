from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename

import subtitle

app = Flask(__name__)

UPLOAD_FOLDER = 'tmp/'
ALLOWED_EXTENSIONS = ['srt', 'txt']

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename, index):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] == ALLOWED_EXTENSIONS[index]

def ext(filename):
	if '.' in filename:
		return filename.rsplit('.', 1)[1]
	else:
		return ""

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/upload", methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
		files = []
		files.append(request.files['srt'])
		files.append(request.files['cut'])
		srtFile = None
		cutFile = None
		for i in range(len(files)):
			file = files[i]
			if file and allowed_file(file.filename, i):
				print file.filename
				filename = secure_filename(file.filename)
				file.save(UPLOAD_FOLDER + filename)
				if ext(filename)=='srt':
					srtFile = filename
				else:
					cutFile = filename
		if not cutFile or not srtFile:
			return "invalid input file"
        dest = subtitle.main(srtFile, cutFile, UPLOAD_FOLDER)
        return redirect(url_for('uploaded_file', filename=dest))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
	return send_from_directory(UPLOAD_FOLDER, filename)
    

if __name__ == "__main__":
    app.run(debug=True)