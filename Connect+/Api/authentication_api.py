import pymysql
import requests
import json
import smtplib,ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
#import clx.xms
import random
import math
from flask import jsonify


otp = "" 
mobile = ""
password = ""
username = ""

mydb = pymysql.connect(
  host="localhost",
  user="root",
  password="admin",
  database="farmaid"
)


def new_user(data): 
    #output = otp_func() 
    #print(output["otp"])
    #if(output["status"] == "success"):
    global otp,mobile,password,username
    mobile = data["mobile"]
    password = data["password"]
    username = data["name"]
    output = {"status": "success"}
    add_user_to_db()
    return jsonify(output)
  


def verify_otp(data):
    global otp
    user_input = data["otp"]
    if otp == user_input:
        print(otp,user_input)
        add_user_to_db()
        output = {"status": "success"}
        return jsonify(output)
    else:
        print(otp,user_input)
        output = {"status": "failed"}
        return jsonify(output)

        
def add_user_to_db():

    global mobile, password,mydb 
    mycursor = mydb.cursor()


    sql = "INSERT INTO user_details (mobile,name,password) VALUES (%s, %s,%s)"
    val = (mobile,username,password)
    mycursor.execute(sql, val)

    mydb.commit()
    return 

def login(data):
    
    global mydb
    mycursor = mydb.cursor()

    mycursor.execute("select user_key,name from user_details where mobile = '"+str(data["mobile"])+"' and password ='"+str(data["password"])+"'")
    myresult = list(mycursor.fetchall())
    if len(myresult) == 0:
        return({"status":"failed"})
    else:
        user_info = myresult
        print(user_info[0])
        return({"status":"success","user_info":list(user_info[0])})


def otp_func():
    OTP = send_otp_mobile()
    print(OTP)
    return({"status":"success","otp" : OTP})


def generateOTP() : 
    # Declare a string variable   
    # which stores all string  
    string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()+_-='
    OTP = "" 

    length = len(string) 
    for i in range(random.randint(5,10)) : 
        OTP += string[math.floor(random.random() * length)] 
    
    return OTP


def send_otp_mobile():
    client = clx.xms.Client(service_plan_id='7dbb615abf724082bfe34217efb937ea', token='e81b7a0c92224ebaa30b2dc9d2de215b')
    create = clx.xms.api.MtBatchTextSmsCreate()
    create.sender = '447537404817'
    create.recipients = {'918124198950'}
    otp_text = generateOTP()
    create.body = otp_text+ " is the OTP"

    try:
        batch = client.create_batch(create)
    except (requests.exceptions.RequestException,
        clx.xms.exceptions.ApiException) as ex:
        print('Failed to communicate with XMS: %s' % str(ex))

    return otp_text


def email_confirmation(receiver_mail, data):
    
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "rithishtemp@gmail.com"  # Enter your address
    receiver_email = receiver_mail
    message = MIMEMultipart("alternative")
    message["Subject"] = "Registration Portal"
    message["From"] = sender_email
    message["To"] = receiver_email
    password = ""
    text = """\
    """+ data["message"] +"""."""
    part1 = MIMEText(text, "plain")
    message.attach(part1)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

    output = {"status": 200}
    return "success"


