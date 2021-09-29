import pymysql
import json

def add_farm(content, key, cropname, name):
    
    db = pymysql.connect( 
    host='localhost', 
    user='root',  
    password = 'admin', 
    db='farmaid'
    ) 
    print("database connected")
    cursor = db.cursor()

    get_user_det = "INSERT INTO polygonStore (polyinfo, clientID, active, farm_name, crop) VALUES (%s, %s, %s, %s, %s);"
    cursor.execute(get_user_det, (json.dumps(content), key, 1, name, cropname))
    db.commit()

    rowid = cursor.lastrowid
    cursor.execute('select * from polygonStore')    
    #user_det = cursor.fetchall()

    print(rowid)
    db.close()
    return rowid

def fetch_farms(key):

    db = pymysql.connect( 
    host='localhost', 
    user='root',  
    password = 'admin', 
    db='farmaid'
    ) 
    print("database connected")
    cursor = db.cursor()

    get_user_det = "SELECT id, farm_name FROM polygonStore WHERE clientID = %s"
    cursor.execute(get_user_det, (key))
    user_farms = cursor.fetchall()

    farm_li = []
    for i in user_farms:
        det = {}
        det['farmid'] = i[0]
        det['farmname'] = i[1]
        farm_li.append(det)
    #print(farm_li)

    return farm_li

def single_farm(farmid):
    
    db = pymysql.connect( 
    host='localhost', 
    user='root',  
    password = 'admin', 
    db='farmaid'
    ) 
    print("database connected")
    cursor = db.cursor()

    get_user_det = "SELECT polyinfo FROM polygonStore WHERE id = %s"
    cursor.execute(get_user_det, (farmid))
    user_farm = cursor.fetchall()
    return user_farm[0][0]


def fetch_details(farmid):

    db = pymysql.connect( 
    host='localhost', 
    user='root',  
    password = 'admin', 
    db='farmaid'
    ) 
    cursor = db.cursor()

    get_farm_det = "SELECT farm_name, crop FROM polygonStore WHERE id = %s"
    cursor.execute(get_farm_det, (farmid))
    user_farm = cursor.fetchall()
    return list(user_farm[0])

def enter_task(userid, farmid, title, seton, about, priority):

    db = pymysql.connect( 
    host='localhost', 
    user='root',  
    password = 'admin', 
    db='farmaid'
    ) 
    cursor = db.cursor()

    qry = "INSERT INTO tasksSchedule (user_id, farmid, title, seton, about, priority) VALUES (%s, %s, %s, %s, %s, %s);"
    cursor.execute(qry, (userid, farmid, title, seton, about, priority))
    db.commit()

def get_task(userid):

    db = pymysql.connect( 
    host='localhost', 
    user='root',  
    password = 'admin', 
    db='farmaid'
    ) 
    cursor = db.cursor()

    qry = "SELECT title, seton, about, task_id, farmid, priority FROM tasksSchedule WHERE user_id = %s"
    cursor.execute(qry, (userid))   
    tasks = cursor.fetchall()
    li = []
    for i in tasks:
        li.append(list(i))
    #print(li)
    return li

def delete_task(taskid):
    
    db = pymysql.connect( 
    host='localhost', 
    user='root',  
    password = 'admin', 
    db='farmaid'
    ) 
    cursor = db.cursor()

    qry = "DELETE FROM tasksSchedule where task_id = %s"
    cursor.execute(qry, (taskid))   
    tasks = cursor.fetchall()

    db.commit()

"""
content = {
"type": "FeatureCollection",
"name": "C01",
"crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
"features": [
{ "type": "Feature", "properties": { "Name": "Shivananjappa - Sorghum", "tessellate": -1, "extrude": 0, "visibility": -1, "fid": 1.0, "layer": "C01 C01.kml", "Area": 1.61095216425805 }, "geometry": { "type": "Polygon", "coordinates": [ [ [ 76.8069496, 11.9317645, 0.0 ], [ 76.806971, 11.9316123, 0.0 ], [ 76.808111, 11.9315887, 0.0 ], [ 76.8081217, 11.9320532, 0.0 ], [ 76.8069013, 11.9320663, 0.0 ], [ 76.8069496, 11.9317645, 0.0 ] ] ] } }
]
}
"""
#print(add_farm(content, 0000))
#fetch_farms(0)
#single_farm(15)
