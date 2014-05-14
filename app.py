import os
from flask import Flask, render_template, send_from_directory
import urllib2
import json
from tracker import *
from bs4 import BeautifulSoup
from nocache import nocache
import time, threading

# initialization
app = Flask(__name__)
app.config.update(
    DEBUG = True
)

def mycron(sid):
    print "Creating new JSON files"
    print createJSON(sid,"1")
    print createJSON(sid,"2")
    threading.Timer(60, mycron(sid)).start()

# controllers
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'ico/favicon.ico')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/")
@nocache
def index():
    return render_template('index.html')

@app.route("/process")
@nocache
def process():
    buses = trackBuses("S1","1")
    with open('data/S1.json', 'w') as fp:
      json.dump(buses, fp)
    return render_template('index.html')

# launch
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    mycron("S1")
    mycron("S2")
