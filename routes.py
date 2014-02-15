from flask import Flask, render_template, json, request
import numpy as np

import matplotlib
import json
import random

matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.ioff()

from threading import Lock
lock = Lock()
import datetime
import mpld3

x = range(100)
y = [a * 2 + random.randint(-20, 20) for a in x]

pie_fracs = [20, 30, 40, 10]
pie_labels = ["A", "B", "C", "D"]


def draw_fig(fig_type):
    """Returns html equivalent of matplotlib figure

    Parameters
    ----------
    fig_type: string, type of figure
            one of following:
                    * line
                    * bar

    Returns
    --------
    d3 representation of figure
    """

    with lock:
        fig, ax = plt.subplots()
        if fig_type == "line":
            ax.plot(x, y)
        elif fig_type == "bar":
            ax.bar(x, y)
        elif fig_type == "pie":
            ax.pie(pie_fracs, labels=pie_labels)
        elif fig_type == "scatter":
            ax.scatter(x, y)
        elif fig_type=="hist":
            ax.hist(y, 5, normed=1, alpha=0.4)


    return mpld3.fig_to_d3(fig)

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/query', methods=['POST'])
def query():
    data = json.loads(request.data)
    return draw_fig(data["plot_type"])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
