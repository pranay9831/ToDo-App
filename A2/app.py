from flask import Flask
import requests
from flask import request
import boto3

s3uri="https://csci5409-assignment2-b00932030.s3.amazonaws.com/test.txt"
FILE_KEY="test.txt"
PROFESSOR_URL='http://52.91.127.198:8080/start'

app = Flask(__name__)


s3=boto3.client('s3', aws_access_key_id="ASIAV27SAQNEXC3ALLMM",
aws_secret_access_key="87b+TdiLebeTrym3RZcjnHnPJQjjjNPeuLGUngca",
aws_session_token="FwoGZXIvYXdzEGwaDEMKJhpXQ9sbMXQQHyLAAX36ggkmERZ0r7uONiGBD6IDn1mI/vVBU2qkdIzwffvl0AndzoD4mdaVqlc/S6zuQBU/HoyAAIKyNNyay20bd3heu9l3InW0DxXvLR+MonECgf+cZcNBSzQmJ/WkrgqVR67as4N3w9sz6sY6nv2FUgpZ/sESRb63trFZhLKGDAJaOaqR0KCZl8zBmRMfSzGepna8VaLKj7rZr45AmbSRCTQ80Ap2lVC+mFRvb4HVjlILIM3CZ7JlfRHt/BIHB96c6yjY6N6fBjItwPAdDzY+Vej7XwX8p7RujRAAMOsPEF9aHO/n9UW6RaIOWBvtjs3fs24tV6jV")

BUCKET_NAME='csci5409-assignment2-b00932030'

@app.route('/start', methods=['GET', 'POST'])
def start():
    try:
        if request.method=="POST":  
            req_json=request.json
            res = requests.post('http://127.0.0.1:5000/start', json=req_json)
            return res.text
        
    except Exception as e:
        print("Exception")
        print(str(e))
        return 400

@app.route('/storedata', methods = ['GET', 'POST'])

def write_file():
    try: 
        if request.method=="POST":
            req_json=request.json
            data=req_json["data"]
            s3.put_object(
                Body=data,
                Bucket=BUCKET_NAME,
                Key=FILE_KEY
            )
          
        return {
            "s3uri":s3uri
        }
    except Exception as e:
        print("Exception")
        print(str(e))
        return 400

@app.route('/appenddata', methods = ['GET', 'POST'])
def append_data():
    try: 
        if request.method=="POST":
            req_json=request.json
            dataToAppend=req_json["data"]

            result = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=FILE_KEY)

            if 'Contents' in result:
                obj=s3.get_object(Bucket=BUCKET_NAME, Key=FILE_KEY)
                dataExisting=obj['Body'].read().decode('utf-8')
                content= dataExisting + dataToAppend
                s3.put_object(
                    Body=content,
                    Bucket=BUCKET_NAME,
                    Key=FILE_KEY
                )
                return {
                    "s3uri":s3uri
                }

                
            else:
                return "Key doesn't exist in the bucket."

            

         
        
    except Exception as e:
        print("Exception")
        print(str(e))
        return 400

@app.route('/deletefile', methods = ['GET', 'POST'])

def delete_file():
    try: 
        if request.method=="POST":
            result = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=FILE_KEY)
            if 'Contents' in result:
                s3.delete_object(Bucket=BUCKET_NAME, Key=FILE_KEY)
          
                return "Successfully deleted"
            else:
                return "Key doesn't exist in the bucket."
    except Exception as e:
        print("Exception")
        print(str(e))
        return 400
