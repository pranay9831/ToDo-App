import base64
import json

from flask import Flask, request,jsonify

import cryptography
from cryptography.hazmat.primitives import serialization, padding, hashes
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

import requests

app = Flask(__name__)

with open('private_key.txt', 'rb') as f:
    private_key = cryptography.hazmat.primitives.serialization.load_pem_private_key(
        f.read(),
        password=None,
    )

with open('public_key.txt', 'rb') as f:
    public_key = cryptography.hazmat.primitives.serialization.load_pem_public_key(
        f.read(),
    )


@app.route('/start', methods=['GET', 'POST'])
def start():
    try:
        if request.method=="POST":  
            req_json=request.json
            res = requests.post('http://44.202.179.158:8080/start', json=req_json)
            return res.text
        
    except Exception as e:
        print("Exception")
        print(str(e))
        return 400


@app.route('/decrypt', methods=['POST'])
def decrypt():
    # Get encrypted data from request
    try:
        # Read private key from file
        with open('private_key.txt', 'r') as f:
            private_key = RSA.import_key(f.read())

        # Get encrypted data from JSON request
        encrypted_data = base64.b64decode(request.json['message'].encode())

        # Decrypt the data
        cipher = PKCS1_OAEP.new(private_key)
        decrypted_data = cipher.decrypt(encrypted_data)

      
        
    
     # Return decrypted data
        return json.dumps({'response': decrypted_data.decode()}), 200

    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/encrypt', methods=['POST'])
def encrypt():
    try:
            # Read public key from file
            with open('public_key.txt', 'r') as f:
                public_key = RSA.import_key(f.read())

            # Get data from JSON request
            data = request.json['message'].encode()

            # Encrypt the data
            cipher = PKCS1_OAEP.new(public_key)
            encrypted_data = cipher.encrypt(data)

    
    
             # Return decrypted data
            return json.dumps({'response': base64.b64encode(encrypted_data).decode()}), 200

    except Exception as e:
        return jsonify({'error': str(e)})



if __name__ == '__main__':
    app.run(debug=True)

