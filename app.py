from flask import Flask, render_template, request, send_file
import os
from huffman import compress, decompress

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/compress')
def compress_page():
    return render_template('compress.html')

@app.route('/decompress')
def decompress_page():
    return render_template('decompress.html')

@app.route('/compress', methods=['POST'])
def compress_route():
    file = request.files['file']
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    output_path = input_path + '.bin'
    file.save(input_path)
    compress(input_path, output_path)
    return send_file(output_path, as_attachment=True)

@app.route('/decompress', methods=['POST'])
def decompress_route():
    file = request.files['file']
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    output_path = input_path + '.txt'
    file.save(input_path)
    decompress(input_path, output_path)
    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
