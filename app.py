# third party imports here
from flask import Flask, jsonify, request
from flask_restful import Resource, reqparse, Api
from flask_cors import CORS

# internal imports here
from hubspot_service import hs_apis

app = Flask(__name__,static_folder="dist")
app.secret_key = b'f0c58e8a-17c6-4edd-af32-cfb265e2cdc2'
CORS(app)
api = Api(app)

app.register_blueprint(hs_apis.hs_bp, url_prefix='/hs')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
