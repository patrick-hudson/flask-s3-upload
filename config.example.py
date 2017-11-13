import os

S3_BUCKET = ""
S3_KEY = ""
S3_SECRET = ""
S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)

SECRET_KEY = os.urandom(32)
AUTH_HEADER = ""
DEBUG = True
PORT = 5000
