from flask import Flask, render_template

app = Flask(__name__)


# Route for default page
@app.route('/')
def home():
    return render_template('dashboard.html')


# Route for dashboard page
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


# Route for upload page
@app.route('/upload')
def upload():
    return render_template('upload.html')