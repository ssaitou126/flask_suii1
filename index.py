import base64
from io import BytesIO
import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt
from flask import Flask, render_template

app = Flask(__name__)

def fig_to_base64_img(fig):
    io = BytesIO()
    fig.savefig(io, format="png")
    io.seek(0)
    base64_img = base64.b64encode(io.read()).decode()

    return base64_img

url = 'http://www1.river.go.jp/cgi-bin/DspWaterData.exe?\
KIND=2&ID=302082182211130&BGNDATE=20230101&ENDDATE=20231231&KAWABOU=NO'

def create_graph():
    dfs = pd.read_html(url)
    df = dfs[1].iloc[2:30,1:].replace(['^(?![+-]?(?:\d+\.?\d*|\.\d+)).+$'],'NaN',regex=True)
    arr = np.array(df,dtype=float).ravel()
    grf = pd.Series(arr)
    smin = grf.min()
    smax = grf.max()
    x = [*range(0,672)]
    fig = plt.figure(figsize=(12,4))
    plt.plot(grf)
    plt.fill_between(x,grf,smin-0.2,color='c',alpha=0.2)
    plt.xticks(np.arange(0, 744, 24),np.arange(1,32))
    plt.ylim(smin-0.2,smax+0.2)
    plt.subplots_adjust(top=1)
    plt.grid()

    return fig

@app.route("/")
def hello():
    fig = create_graph()
    img = fig_to_base64_img(fig)

    return render_template("index.html", img=img)
