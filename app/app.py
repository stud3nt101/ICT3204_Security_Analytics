import json

import logs

from flask import Flask, render_template, redirect, jsonify

app = Flask(__name__)


# Route for default page
@app.route('/')
def home():
    return redirect('/dashboard')


# Route for dashboard page
@app.route('/dashboard')
def dashboard():
    test_ip = {'192.10.3.2': "10", '172.10.3.2': "500", "172.10.3.1": "232", "172.10.5.1":"324"}
    return render_template('dashboard.html', ip=test_ip)


@app.route('/authlog')
def authlog():
    # Change file
    log_data, col = logs.authlog("./Logs/webserver_auth.log")
    return render_template('auth_logs.html', col=col, logdata=log_data)


@app.route('/histlog')
def histlog():
    log_data, col = logs.histlog(".\Logs\webserver_history_with_TS.log")
    return render_template('hist_logs.html', col=col, logdata=log_data)


# Route for upload page
@app.route('/upload')
def upload():
    return render_template('upload.html')