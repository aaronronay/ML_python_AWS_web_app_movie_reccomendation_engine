from flask import Flask, jsonify, render_template, url_for
from scrape import theater_scrape
#from user_choice import zipcode_select
import os
import pandas as pd
import numpy as np


#Flask Initialize
print('Now starting flask server')
app = Flask(__name__)


@app.route("/")
def index():
    '''Return to the homepage.'''
    return render_template('index_map.html')


@app.route('/scrape')
def scrape():
    return jsonify(theater_scrape())



if __name__ == "__main__":
    app.run()
    url_for('static/scrape', filename='result.json') #if there is an existing json file in the static folder

# if __name__ == "__main__":
#     app.run()


