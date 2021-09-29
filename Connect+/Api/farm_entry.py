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


def new_entry(data): 
    mycursor = mydb.cursor()
    sql = "INSERT INTO entryTable (user_id  ,entry_name ,farm_id , irrigation, pesticide ,fertilizer , time,comments ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (data["user_key"],data["name"],data["farm_id"],data["irrigation"],data["pesticide"],data["fertilizer"],data["date"],data["comments"])
    mycursor.execute(sql, val)

    mydb.commit()
    output = {"status": "success"}
    return jsonify(output)


def previous_entry(data): 
    mycursor = mydb.cursor()
    sql = "select * from entryTable where user_id ="+data["user_key"]+" and farm_id="+data["farm_id"]+" Order by entry_id DESC"
    mycursor.execute(sql)
    myresult = list(mycursor.fetchall())
    if len(myresult) == 0:
        return({"status":"no previous entries"})
    else:
        user_info = myresult
        print(user_info[0])
        return({"status":"success","user_info":user_info[0]})
    output = {"status": "success"}
    return jsonify(output)

def widget_info(data): 
    mycursor = mydb.cursor()
    sql = "select COUNT(*) from entryTable where user_id ="+data["user_key"]+" and farm_id="+data["farm_id"]
    mycursor.execute(sql)
    myresult = list(mycursor.fetchall())
    if len(myresult) == 0:
        output = {"status":"no previous entries","no_of_entries":0}
        return(output)
    else:
        user_info = myresult
        print(user_info[0])
        output = {"no_of_entries":user_info[0]}
    
    sql = "select time from entryTable where user_id ="+data["user_key"]+" and farm_id="+data["farm_id"]+" and irrigation=True Order by entry_id DESC"
    mycursor.execute(sql)
    myresult = list(mycursor.fetchall())
    if len(myresult) == 0:
        output["irrigation"] = "No previous value"
    else:
        user_info = myresult
        print(user_info[0])
        output["irrigation"] = user_info[0]
    
    sql = "select time from entryTable where user_id ="+data["user_key"]+" and farm_id="+data["farm_id"]+" and fertilizer=True Order by entry_id DESC"
    mycursor.execute(sql)
    myresult = list(mycursor.fetchall())
    if len(myresult) == 0:
        output["fertilizer"] = "No previous value"
    else:
        user_info = myresult
        print(user_info[0])
        output["fertilizer"] = user_info[0]
    
    sql = "select time from entryTable where user_id ="+data["user_key"]+" and farm_id="+data["farm_id"]+" and pesticide=True Order by entry_id DESC"
    mycursor.execute(sql)
    myresult = list(mycursor.fetchall())
    if len(myresult) == 0:
        output["pesticide"] = "No previous value"
    else:
        user_info = myresult
        print(user_info[0])
        output["pesticide"] = user_info[0]
    
    output["status"] = "success"
    mycursor.close()
    return jsonify(output)

