from flask import Flask, render_template, url_for,request,redirect
from flask_bootstrap import Bootstrap
from Features import Features, ANN
import cv2
import os
from werkzeug.utils import secure_filename
from flask import send_from_directory

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

#ML Packages


app = Flask(__name__)
Bootstrap(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def index():
    return render_template('index.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            error = "Choose image first."
            print('No file part')
            return render_template('index.html', error=error)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without file'name
        if file.filename == '':
            error = "Choose image first."
            print('No selected file')
            return render_template('index.html', error=error)
        if file and allowed_file(file.filename):
            print("aa ")
            upload_img = secure_filename(file.filename)
            print(upload_img)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], upload_img))
            # print(app.config['UPLOAD_FOLDER'])
            #return redirect(url_for('uploaded_file',
                                    #filename=filename))

            #image = cv2.imread('31.jpg')
            #image = cv2.imread(url_for('uploaded_file', filename=filename))
            image = cv2.imread(upload_img)
            #cv2.imshow("median", image)

            #call image feature extraction function

            im = Features(image) #extract image features and identifying  pepper kind whether is it black pepper or white pepper
            ppr, data = im.segmentation()
            print("Pepper kind:", ppr)

            # call artificial neural network model and classification algorithm
            ann = ANN(ppr, data) #classify into seed posibilities
            grade = ann.classification()
            print("Grade:", grade)
            return render_template('result.html', image_name=upload_img, grade=grade, ppr=ppr)
        else:
            error = "Please upload image in png , jpeg or jpg format."
            print(error)
            return render_template('index.html', error=error)

    # if request.method == 'POST':
    #
    #     # target = os.path.join(APP_ROOT, 'static/')
    #     # print(target)
    #     # if not os.path.isdir(target):
    #     #     os.mkdir(target)
    #     #
    #     # else:
    #     #     print("Couldn't create upload directory: {}".format(target))
    #     # print(request.files.getlist("file"))
    #     # for upload in request.files.getlist("file"):
    #     #     print(upload)
    #     #     filename = upload.filename
    #     #     destination = "/".join([target, filename])
    #     #     upload.save(destination)
    #     #
    #     # return render_template('result.html', image_name=filename)
    #
    #
    #    # text = request.form['namequery']
    #
    #     image = request.files['image']
    #     return render_template('result.html', image_name=image)
    #    #image = cv2.imread('static/image/31.jpg')
    #    #im = Features(image)
    #    #ppr, data = im.segmentation()
    #    #print("Pepper kind:", ppr)
    #
    #    #ann = ANN(ppr, data)
    #    #grade = ann.classification()
    #    #print(grade)



if __name__ == '__main__':
    app.run(debug=True)
