import flask
from flask import request, jsonify
from flask_cors import CORS, cross_origin
from api_db import add_farm, fetch_farms, single_farm, fetch_details, enter_task, get_task, delete_task
from authentication_api import new_user,verify_otp,login
from farm_entry import new_entry,previous_entry, widget_info
import json
import requests
import datetime 



app = flask.Flask(__name__,template_folder='template')
app.config["DEBUG"] = True
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#API homepage

@app.route('/', methods=['GET'])
def home():
    return '''<h1>API homepage</h1>
<p>API for Farming</p>'''

#To upload Polygon this method will be used

@app.route('/postjson', methods = ['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def postJsonHandler():

    query_parameters = request.args
    key = query_parameters.get('key')

    content = request.get_json()
    #print(type(content))
    #content = json.loads(content_str)
    name = content['name']
    print(name)

    rows = add_farm(content, key, content['cropname'],name)
    json_op = {"id":rows, "farm_name":name}
    return jsonify(json_op)

@app.route('/userfarms', methods = ['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def user_farms():

    query_parameters = request.args
    key = query_parameters.get('key')

    return jsonify({"Active":fetch_farms(key)})

@app.route('/showfarm', methods = ['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def show_farm():

    query_parameters = request.args
    farmid = query_parameters.get('farmid')

    geoj_str = single_farm(farmid)
    #print(type(geoj_str))
    geoj = json.loads(geoj_str)
    return jsonify({"coordinates":[geoj['geo_json']['geometry']['coordinates'][0]]})

@app.route('/name_crop', methods = ['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def details():

    query_parameters = request.args
    key = query_parameters.get('farmid')

    return jsonify({"farmname":fetch_details(key)[0], "crop":fetch_details(key)[1]})

@app.route('/weather', methods = ['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def weather_fun():

    query_parameters = request.args
    farmid = query_parameters.get('farmid')

    geoj_str = single_farm(farmid)
    #print(type(geoj_str))
    geoj = json.loads(geoj_str)
    lon = geoj['geo_json']['geometry']['coordinates'][0][0][0]
    lat = geoj['geo_json']['geometry']['coordinates'][0][0][1]

    url = ("""https://api.openweathermap.org/data/2.5/onecall?lat=""" + str(lat) + """&lon="""+ str(lon) + 
            """&exclude=hourly,minutely&appid=bc7200ffb0d757c0c0b7daa8c61ac7ce""")
    
    r = requests.get(url = url)
    data = r.json()
    print(data['daily'][0]['temp'])

    #res = {}
    li = []
    for i in data['daily']:
        sub = {}
        timestamp = datetime.datetime.fromtimestamp(i['dt'])
        sub['date'] = timestamp.strftime('%d-%m-%Y')
        sub['min'] = i['temp']['min']
        sub['max'] = i['temp']['max']
        sub['day'] = i['temp']['day']
        sub['desc'] = i['weather'][0]['description']
        li.append(sub)

    return jsonify ({"result_weather":li})

@app.route('/newtask', methods = ['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def new_task():

    query_parameters = request.args
    userid = query_parameters.get('userid')
    farmid = query_parameters.get('farmid')
    data = request.get_json()

    enter_task(userid, farmid, data['title'], data['seton'], data['about'], data['priority'])

    return jsonify({"Status":"Success"})

@app.route('/fetchtasks', methods = ['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def fetch_tasks():

    query_parameters = request.args
    userid = query_parameters.get('userid')

    tasks = get_task(userid)
    date_today = datetime.date.today()
    print(date_today)
    pending = []
    rem = []
    #return jsonify({"Mess":"Ji"})
    for i in tasks:
        date_time_obj = datetime.datetime.strptime(i[1], '%Y-%m-%d').date()
        if date_time_obj < date_today:
            pending.append({"title":i[0], "seton":i[1], "desc":i[2], "tid":i[3], "name":fetch_details(i[4])[0], "farmid":i[4], "priority":i[5]})
        else:
            rem.append({"title":i[0], "seton":i[1], "desc":i[2], "tid":i[3], "name":fetch_details(i[4])[0], "farmid":i[4], "priority":i[5]})
    
    return jsonify({"pending":pending, "remaining":rem})

@app.route('/deltask', methods = ['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def del_task():

    query_parameters = request.args
    taskid = query_parameters.get('taskid')

    delete_task(taskid)

    return jsonify({"Status":"Success"})

@app.route("/new_user", methods=["POST", "GET"])
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def create_new_user():
    data = request.get_json()
    return new_user(data)


@app.route("/verify_otp", methods=["POST", "GET"])
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def verify_the_otp():
    data = request.get_json()
    return verify_otp(data)


@app.route("/login", methods=["POST", "GET"])
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def logging_in():
    data = request.get_json()
    print(data)
    return login(data)

@app.route("/postentry", methods=["POST", "GET"])
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def post_entry():
    data = request.get_json()
    return new_entry(data)

@app.route("/previousentry", methods=["POST", "GET"])
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def previous_entries():
    data = request.get_json()
    return previous_entry(data)

@app.route("/widgets", methods=["POST", "GET"])
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def widgets():
    data = request.get_json()
    return widget_info(data)


app.run(host='192.168.0.103', port = 8001)
