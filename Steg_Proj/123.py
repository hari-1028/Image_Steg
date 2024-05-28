from flask import Flask, render_template, send_file, request
import os
from Encode import encode
from Decode import decode
from PIL import Image

app = Flask(__name__)

RESULTS_DIR = os.path.join(os.getcwd(), "static/results")
if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)

@app.route('/')
def index():
    try:
        os.remove('static/results/input.png')
        os.remove('static/results/output.png')
        os.remove('static/results/inbyus4dec.png')
        os.remove('output.png')
    except:
        print("***")
    return render_template('Home.html')

@app.route('/nav2enc')
def navenc():
    return render_template("Enc.html")

@app.route('/downencimage')
def download():
    p = os.path.join(RESULTS_DIR, 'output.png')
    return send_file(p, as_attachment=True)

@app.route('/nav2dec')
def navdec():
    return render_template("Dec.html")

@app.route('/content', methods=['POST'])
def encode_message():
    msg = request.form['msg']
    password = request.form['pw']
    f = request.files['image']
    inputimgpath = os.path.join(os.getcwd(), f.filename)
    f.save(inputimgpath)
    try:
        image = Image.open(inputimgpath)
    except IOError:
        return render_template('Home.html', error="Please upload a valid image file.")
    image = image.convert('RGB')
    image.save(os.path.join(RESULTS_DIR, "input.png"))
    image = Image.open(inputimgpath)
    image = image.convert('RGB')
    image.save(os.path.join(RESULTS_DIR, "output.png"))
    print("Image successfully converted!")
    os.remove(inputimgpath)
    encode(msg, password)
    os.remove(os.path.join(RESULTS_DIR, 'input.png'))
    return render_template('Enc_image.html', msg=msg, message="Encrypted successfully")

@app.route('/contdec', methods=['POST'])
def decode_message():
    password = request.form['pw']
    f = request.files['file']
    inputimgpath4dec = os.path.join(RESULTS_DIR, f.filename)
    f.save(inputimgpath4dec)
    try:
        image = Image.open(inputimgpath4dec)
    except IOError:
        return render_template('Home.html', error="Please upload a valid image file.")
    image = image.convert('RGB')
    image.save(os.path.join(RESULTS_DIR, "inbyus4dec.png"))
    message = decode(password)
    return render_template('Dec_image.html', msg=message)

if __name__ == '__main__':
    app.run(debug=True)
