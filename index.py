# -*- coding: utf-8 -*-
from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

def pdread():
	dfs = pd.read_html('http://www1.river.go.jp/cgi-bin/DspWaterData.exe?KIND=2&ID=302082182211040&BGNDATE=20230101&ENDDATE=20231231&KAWABOU=NO')
	return dfs[0]
result = pdread()

@app.route('/')
def index():
	title = '米代川'
	framework = result
	return render_template('index.html', title=title, framework=framework)

if __name__ == '__main__':
	app.run()