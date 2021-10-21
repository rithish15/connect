import flask
from flask import request, jsonify
from flask_cors import CORS, cross_origin
from AES_module import AES
from ECC_module import ECC

from Convert import converter
import ast
from random import randint
import requests
from urllib.request import urlopen
import json

#flask Config
app = flask.Flask(__name__,template_folder='templates')
app.config["DEBUG"] = True
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

aes_key = ""
ecc_public = ""
ecc_private_d = ""
C1_aesKey = ""
C2_aesKey = ""
C1_multimedia = ""
C2_multimedia = ""

# 2
def encryption(uid,file_name):
    ecc_obj_AESkey = ECC.ECC()
    (C1_aesKey, C2_aesKey) = ecc_obj_AESkey.encryption(ast.literal_eval(ecc_public), str(int(aes_key)))
    print(C1_aesKey,C2_aesKey)
    print("-------------------------------------------------------------------------")

    file = "./uploads/"+file_name
    multimedia_data = converter.fileToBase64(str(file))
    aes = AES.AES(int(aes_key))
    encrypted_multimedia = aes.encryptBigData(multimedia_data)
    data_for_ecc = converter.makeSingleString(encrypted_multimedia)
    ecc = ECC.ECC()
    (C1_multimedia, C2_multimedia) = ecc.encryption(ast.literal_eval(ecc_public), data_for_ecc) 
    print(C1_multimedia)
    print("C2_multimedia--------------------------------------------")
    print(C2_multimedia)
    print("-------------------------------------------------------------------------")
    url = 'http://192.168.0.103:8002/save_file'
    data = {"C1_aesKey":C1_aesKey,"C2_aesKey": C2_aesKey,"C1_multimedia" :C1_multimedia, "C2_multimedia" :C2_multimedia,"File_name" :file_name,"User_id" :uid}
    r = requests.post(url,verify=False, json=data)
    if (r.status_code == 200):
        print("Successfully uploaded file")
    return

# @app.route("/new_user", methods=["POST", "GET"])
# @cross_origin(origin="*", headers=["Content-Type", "Authorization"])
# def create_new_user():
#     data = request.get_json()
#     print(data)
#     return new_user(data)

# @app.route("/login", methods=["POST", "GET"])
# @cross_origin(origin="*", headers=["Content-Type", "Authorization"])
# def logging_in():
#     data = request.get_json()
#     print(data)
#     return login(data)


@app.route("/upload", methods=["POST", "GET"])
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def file_upload():
    query_parameters = request.args
    uid = query_parameters.get('userid')
    file_name = query_parameters.get('fname')
    global aes_key,ecc_public
    aes_key = randint(10,99)
    output = urlopen('http://192.168.0.103:8002/get_ecc_public')
    data_json = json.loads(output.read().decode('utf-8'))
    ecc_public = str(data_json['ecc_public_key'])
    print(aes_key,ecc_public)
    print(uid,file_name)
    encryption(uid,file_name)
    return "success"

#download
def public_key_generation_d(ecc_private_key_d):
   ecc_obj_AESkey = ECC.ECC()
   ecc_public_key_d = ecc_obj_AESkey.gen_pubKey(int(ecc_private_key_d))
   ecc_public_d = str(ecc_public_key_d)
   print(ecc_public_d)
   print("-------------------------------------------------------------------------")
   return ecc_public_d

@app.route("/get_ecc_public_download", methods=["POST", "GET"])
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def get_ecc_public():
   global ecc_private_d
   ecc_private_d = str(randint(100,199))
   print(ecc_private_d)
   ecc_public_key_d = public_key_generation_d(ecc_private_d)
   return({"status":"success","ecc_public_key_d":ecc_public_key_d})

# 3
@app.route("/download_file", methods=["POST", "GET"])
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def decrypt():
    data = request.get_json()
    C1_aesKey_d = data["C1_aesKey_d"]
    C2_aesKey_d = data["C2_aesKey_d"]
    C1_multimedia_d = data["C1_multimedia_d"]
    C2_multimedia_d = data["C2_multimedia_d"]
    Uid = data["User_id"]
    file_name =  r".\download\\"+data["File_name"]

    global ecc_private_d

    ecc_AESkey = ECC.ECC()
    decryptedAESkey_d = ecc_AESkey.decryption(C1_aesKey_d, C2_aesKey_d, ecc_private_d)

    ecc_obj = ECC.ECC()
    encrypted_multimedia_d = ecc_obj.decryption(C1_multimedia_d, C2_multimedia_d, ecc_private_d)
    clean_data_list_d = converter.makeListFromString(encrypted_multimedia_d)

    aes_obj = AES.AES(int(decryptedAESkey_d))
    decrypted_multimedia_d = aes_obj.decryptBigData(clean_data_list_d)
    converter.base64ToFile(decrypted_multimedia_d, str(file_name))
    return ({"status":"success"})

if __name__ == "__main__":
    app.run(host='192.168.0.103', port = 8001)