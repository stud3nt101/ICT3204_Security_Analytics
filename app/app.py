import json

from flask import Flask, render_template, redirect

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


# Route for upload page
@app.route('/upload')
def upload():
    return render_template('upload.html')