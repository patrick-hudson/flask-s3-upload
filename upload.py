from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import os
import boto3, botocore
import random, string
app = Flask(__name__)
app.config.from_pyfile('config.py')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'gz', 'tar', 'zip'])
s3 = boto3.client(
   "s3",
   aws_access_key_id=app.config['S3_KEY'],
   aws_secret_access_key=app.config['S3_SECRET']
)
from os.path import splitext
def get_extension(path):
    for ext in ['.tar.gz', '.tar.bz2']:
        if path.endswith(ext):
            return path[:-len(ext)], path[-len(ext):]
    return splitext(path)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def upload_file_to_s3(file, bucket_name, acl="public-read"):
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e
    return "{}{}".format('http://ug.ly/', file.filename)

@app.route('/', methods=['GET'])
def upload_form():
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=user_file>
         <input type=submit value=Upload>
    </form>
    '''
@app.route('/', methods=['POST'])
def upload_file():
    auth_header = request.headers['Authorization']
    if auth_header != app.config['AUTH_HEADER']:
        return "Failed to authenticate\n"
    if "user_file" not in request.files:
        return "No user_file key in request.files\n"

    file = request.files["user_file"]

    """
        These attributes are also available

        file.filename               # The actual name of the file
        file.content_type
        file.content_length
        file.mimetype

    """

	# C.
    if file.filename == "":
        return "Please select a file"

	# D.
    if file and allowed_file(file.filename):
        x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(12))
        fname = get_extension(file.filename)[0]
        ename = get_extension(file.filename)[1]
        file.filename = x + ename
        file.filename = secure_filename(file.filename)
        print(file.filename)
        output   	  = upload_file_to_s3(file, app.config["S3_BUCKET"])
        return str(output)

    else:
        return redirect("/")

if __name__ == "__main__":
    app.run()
