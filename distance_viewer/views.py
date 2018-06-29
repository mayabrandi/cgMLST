from flask import make_response, flash, abort, url_for, redirect, render_template, request, session
from flask_login import login_user,logout_user, current_user, login_required
from flask.ext.mail import Message
from flask_oauthlib.client import OAuthException
from extentions import app
from plot import DistancePlot

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot/')
def sample_page():
    dfile = 'dist_the_one_wgs.txt'
    classifyer = 300
    DP = DistancePlot(dfile, classifyer)
    DP.make_matrix()
    DP.give_2d_positions()
    DP.cluster()
    X = list(DP.positions[:, 0])
    Y = list(DP.positions[:, 1])
    

    return render_template('plot.html',
        X = X,
        Y = Y,
        colors = list(DP.colors),
        labes = list(DP.node_labels),
        classifyer = classifyer
)
