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

threaded_ids = []

def ended():
  print "Cron ended!"

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

@app.route('/<sid>/')
@nocache
def indexbus(sid):
    if sid not in threaded_ids:
      threading.Thread(target=mycron, args=[sid]).start()
      threaded_ids.append(sid)
    return render_template('indexbus.html', sid=sid)

@app.route("/")
@nocache
def index():
    return render_template('index.html')

# launch
if __name__ == "__main__":
    threading.Thread(target=mycron, args=["S2"]).start()
    threading.Thread(target=mycron, args=["500"]).start()
    threaded_ids.append("S2")
    threaded_ids.append("500")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
