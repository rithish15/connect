import flask
from flask import request, jsonify
from flask_cors import CORS, cross_origin
from AES_module import AES
from ECC_module import ECC
from Convert import converter
from authentication_api import new_user,login
import ast
from random import randint
from urllib.request import urlopen
import json
from os import listdir
from os.path import isfile, join
import os.path, time
import requests
import shutil

#flask Config
app = flask.Flask(__name__,template_folder='template')
app.config["DEBUG"] = True
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
ecc_private = ""
aes_key_d = ""
ecc_public_d = ""
C1_aesKey_d = ""
C2_aesKey_d = ""
C1_multimedia_d = ""
C2_multimedia_d = ""

# 1
#ecc public key generation
def public_key_generation(ecc_private_key):
   ecc_obj_AESkey = ECC.ECC()
   ecc_public_key = ecc_obj_AESkey.gen_pubKey(int(ecc_private_key))
   ecc_public = str(ecc_public_key)
   print(ecc_public)
   print("-------------------------------------------------------------------------")
   return ecc_public

@app.route("/get_ecc_public", methods=["POST", "GET"])
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def get_ecc_public():
   global ecc_private
   ecc_private = str(randint(100,199))
   print(ecc_private)
   ecc_public_key = public_key_generation(ecc_private)
   return({"status":"success","ecc_public_key":ecc_public_key})

@app.route("/new_user", methods=["POST", "GET"])
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def create_new_user():
    data = request.get_json()
    print(data)
    return new_user(data)

@app.route("/login", methods=["POST", "GET"])
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def logging_in():
    data = request.get_json()
    print(data)
    return login(data)
    
# 3
@app.route("/save_file", methods=["POST", "GET"])
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def decrypt():
    data = request.get_json()
    C1_aesKey = data["C1_aesKey"]
    C2_aesKey = data["C2_aesKey"]
    C1_multimedia = data["C1_multimedia"]
    C2_multimedia = data["C2_multimedia"]
    Uid = data["User_id"]
    file_name =  r".\Drive\\"+Uid+"\\"+data["File_name"]
    
    global ecc_private

    ecc_AESkey = ECC.ECC()
    decryptedAESkey = ecc_AESkey.decryption(C1_aesKey, C2_aesKey, ecc_private)

    ecc_obj = ECC.ECC()
    encrypted_multimedia = ecc_obj.decryption(C1_multimedia, C2_multimedia, ecc_private)
    clean_data_list = converter.makeListFromString(encrypted_multimedia)

    aes_obj = AES.AES(int(decryptedAESkey))
    decrypted_multimedia = aes_obj.decryptBigData(clean_data_list)
    converter.base64ToFile(decrypted_multimedia, str(file_name))
    return ({"status":"success"})

def encryption_d(uid,file_name):
    ecc_obj_AESkey = ECC.ECC()
    (C1_aesKey_d, C2_aesKey_d) = ecc_obj_AESkey.encryption(ast.literal_eval(ecc_public_d), str(int(aes_key_d)))
    print(C1_aesKey_d,C2_aesKey_d)
    print("-------------------------------------------------------------------------")

    file =file_name
    multimedia_data_d = converter.fileToBase64(str(file))
    aes_d = AES.AES(int(aes_key_d))
    encrypted_multimedia_d = aes_d.encryptBigData(multimedia_data_d)
    data_for_ecc_d = converter.makeSingleString(encrypted_multimedia_d)
    ecc = ECC.ECC()
    (C1_multimedia_d, C2_multimedia_d) = ecc.encryption(ast.literal_eval(ecc_public_d), data_for_ecc_d) 
    print(C1_multimedia_d)
    print("C2_multimedia--------------------------------------------")
    print(C2_multimedia_d)
    print("-------------------------------------------------------------------------")
    url = 'http://192.168.0.103:8001/download_file'
    data = {"C1_aesKey_d":C1_aesKey_d,"C2_aesKey_d": C2_aesKey_d,"C1_multimedia_d" :C1_multimedia_d, "C2_multimedia_d" :C2_multimedia_d,"File_name" :file_name[file_name.rfind('\\')+1:],"User_id" :uid}
    r = requests.post(url,verify=False, json=data)
    if (r.status_code == 200):
        print("Successfully sent file")
    return


@app.route("/download", methods=["POST", "GET"])
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def file_download():
    query_parameters = request.args
    uid = query_parameters.get('userid')
    file_name = query_parameters.get('fname')
    global aes_key_d,ecc_public_d
    aes_key_d = randint(10,99)
    output = urlopen('http://192.168.0.103:8001/get_ecc_public_download')
    data_json = json.loads(output.read().decode('utf-8'))
    ecc_public_d = str(data_json['ecc_public_key_d'])
    print(aes_key_d,ecc_public_d)
    encryption_d(uid, ".\Drive\\"+uid+"\\"+file_name)
    return "success"

@app.route("/fetchfiles", methods=["POST", "GET"])
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def fetch_files():
    query_parameters = request.args
    uid = query_parameters.get('userid')

    mypath = "./Drive/" + str(uid)
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    res = []
    
    for i in onlyfiles:
        tmp = []
        tmp.append(i)
        time1 = time.ctime(os.path.getctime(mypath + "/" + i))
        print(time1)
        tmp.append(time1)
        tmp.append(i.split('.')[1])
        res.append(tmp)
    return jsonify({"res": res})

@app.route("/fetchallpublicfiles", methods=["POST", "GET"])
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def fetch_public_all_files():
    query_parameters = request.args
    uid = query_parameters.get('userid')

    root = "./Public/" 
    onlyfiles = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            print(os.path.join(path, name))
            onlyfiles.append(os.path.join(path, name))
    res = []
    
    for i in onlyfiles:
        tmp = []
        name =  i.split('\\')[1]
        tmp.append(name)
        time1 = time.ctime(os.path.getctime(i))
        print(time1)
        tmp.append(time1)
        tmp.append(i.split('.')[2])
        user = i[i.rfind('/')+1:i.rfind('\\')] 
        tmp.append(user)
        res.append(tmp)
    print(res)
    return jsonify({"res": res})


@app.route("/download_public_file", methods=["POST", "GET"])
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def public_file_download():
    query_parameters = request.args
    uid = query_parameters.get('userid')
    file_name = query_parameters.get('fname')
    global aes_key_d,ecc_public_d
    aes_key_d = randint(10,99)
    output = urlopen('http://192.168.0.103:8001/get_ecc_public_download')
    data_json = json.loads(output.read().decode('utf-8'))
    ecc_public_d = str(data_json['ecc_public_key_d'])
    print(aes_key_d,ecc_public_d)
    encryption_d(uid, ".\Public\\"+uid+"\\"+file_name)
    return "success"


@app.route("/deletefile", methods=["POST", "GET"])
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def delete():
    query_parameters = request.args
    uid = query_parameters.get('userid')
    fname = query_parameters.get('fname')
    path = './Drive/' + uid + '/' + fname
    print(isfile(path))
    os.remove(path)
    return jsonify({"message":"Success"})

@app.route("/make_public", methods=["POST","GET"])
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def makePublic():
    query_parameters = request.args
    uid = query_parameters.get('userid')
    fname = query_parameters.get('fname')
    print(uid,fname)
    src_path = 'C:/Users/rithi/Desktop/Connect+/Connect/server/Drive/' + uid + '/' + fname
    dst_path = 'C:/Users/rithi/Desktop/Connect+/Connect/server/Public/' + uid + '/' + fname
    print(src_path,dst_path)
    shutil.move(src_path, dst_path)
    status_code = flask.Response(status=200)
    return status_code


@app.route("/delete_public_file", methods=["POST", "GET"])
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def delete_public():
    query_parameters = request.args
    uid = query_parameters.get('userid')
    fname = query_parameters.get('fname')
    path = './Public/' + uid + '/' + fname
    print(isfile(path))
    os.remove(path)
    return jsonify({"message":"Success"})

app.run(host='192.168.0.103', port = 8002)