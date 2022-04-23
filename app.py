from imp import source_from_cache
from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

ROVERS = {
    "Curiosity": [
        "FHAZ",
        "RHAZ",
        "MAST",
        "CHEMCAM",
        "MAHLI",
        "MARDI",
        "NAVCAM"
    ],

    "Spirit": [
        "FHAZ",
        "RHAZ",
        "NAVCAM",
        "PANCAM",
        "MINITES"
    ],

    "Opportunity": [ 
        "FHAZ",
        "RHAZ",
        "NAVCAM",
        "PANCAM",
        "MINITES"
    ]
}

rover_name = ''
sol = 0
cam = ''
data = ''

#sol numbers
#5109 opportunity
#2208 spirit
#3450+ curiosity 

@app.route('/')
def index():
    return render_template("index.html", rovers=ROVERS)

@app.route('/submit', methods=["POST"])
def submit():
    global rover_name
    rover_name = request.form.get("rover")
    if rover_name not in ROVERS:
        return render_template("failure.html")
    
    return render_template("camera.html", rovername=rover_name, list=ROVERS[f'{rover_name}'])

@app.route('/submit1', methods=["POST"])
def submit1():
    cam = request.form.get("camera")
    global rover_name
    global data
    global sol

    if cam not in ROVERS[f'{rover_name}']:
        return render_template("failure.html")
    
    sol = request.form.get("number")
    print(sol)

    r = requests.get(f'https://api.nasa.gov/mars-photos/api/v1/rovers/{rover_name}/photos?sol={sol}&camera={cam}&api_key=eeXCbwIsOSMtUqAvdHfQzKHaFR64E1iX5qsjQdsC')

    print(r.ok)

    with open('nasa_pic.json','w') as f:
        f.write(r.text)

    with open('nasa_pic.json','r') as f:
        file_data = json.load(f)

    dict = file_data['photos']

    data = ''
    for value in dict:
        if value['img_src']:
            data = value['img_src']
            break
    
    print(data)
    return render_template("success.html", source=data)

