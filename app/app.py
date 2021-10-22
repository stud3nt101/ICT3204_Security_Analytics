import json
import os
import re

import pandas as pd
from os import system

import logs
import LoadData, ml
import pcap

from flask import Flask, render_template, redirect, request, session

app = Flask(__name__)
app.secret_key = 'e3w5PGoP(P&I%1xm&ogiO#ckF7*DkI3X'

temp_file = []

ALLOWED_EXTENSIONS = set(['pcapng','log'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for default page
@app.route('/', methods=["POST", "GET"])
def home():
    if session.get("authFilename") is not None or session.get("histFilename") is not None or session.get("pcapFilename") is not None:
        return redirect('/dashboard')
    else:
        return redirect('/upload')


@app.route('/upload-process', methods=["POST", "GET"])
def upload_process():
    # Get all files uploaded
    file_list = request.files.getlist("file")
    path = "./upload/"
    check = 0  # To check that the files uploaded meets the requirements

    # Initialize session as empty string
    session['authFilename'] = ""
    session['histFilename'] = ""
    session['pcapFilename'] = ""

    for files in file_list:
        if allowed_file(files.filename) and len(temp_file) < 3:
            temp_file.append(files)
            files.save(path + files.filename)
            check = 1
        else:
            check = 0

    # Create session for files found
    for data in temp_file:
        # AUTH LOG
        if re.match(".*auth\.log", data.filename.lower()):
            session['authFilename'] = path + data.filename
        # HIST LOG
        elif re.match(".*history\.log", data.filename.lower()):
            session['histFilename'] = path + data.filename
        # PCAP FILE
        elif re.match(".*\.pcapng", data.filename.lower()):
            session['pcapFilename'] = path + data.filename
    if check == 1:
        return render_template('upload.html')
    else:
        return redirect('upload.html')


# Route for upload page
@app.route('/upload-complete', methods=["POST", "GET"])
def upload_complete():
    check = None

    for file in temp_file:
        if file.filename.rsplit('.', 1)[1].lower() == "pcapng":
            check = 1
            break

    if len(temp_file) != 0 and check != None:
        for file in temp_file:
            if file.filename.rsplit('.', 1)[1].lower() == "pcapng":
                # require tshark
                # require argus-server
                system(
                    "tshark -r upload/" + file.filename + " -T fields -E header=y -E separator=, -E occurrence=a -E quote=s"
                                                          " -e frame.time -e _ws.col.Protocol -e _ws.col.Length -e tcp.flags -e ip.src -e tcp.srcport -e udp.srcport -e ip.dst"
                                                          " -e tcp.dstport -e udp.dstport -e _ws.col.Info > upload/temp.csv")

                # Precreate an empty temp.biargus file
                system(
                    "argus -F utils/argus.conf -r upload/" + file.filename + " -w temp.biargus | ra -r temp.biargus -n -F utils/ra.conf -Z b > upload/temp.binetflow")

        temp_file.clear()
        return redirect('/dashboard')
    else:
        temp_file.clear()
        if session.get("authFilename") is not '':
            return redirect('/authlog')
        elif session.get("histFilename") is not '':
            return redirect('/histlog')
        else:
            return render_template('upload.html')


# Route for upload page
@app.route('/upload', methods=["POST", "GET"])
def upload():
    if session.get("authFilename") is None or session.get("histFilename") is None or session.get(
            "pcapFilename") is None:
        return render_template('upload.html')
    else:
        return redirect('/dashboard')


# Route for reuploading files page
@app.route('/reupload', methods=["POST"])
def reupload():
    # Pop all existing sessions
    if session.get("authFilename") is not None:
        session.pop("authFilename")
    if session.get("histFilename") is not None:
        session.pop("histFilename")
    if session.get("pcapFilename") is not None:
        session.pop("pcapFilename")
    return render_template('upload.html')


# Route for dashboard page
@app.route('/dashboard')
def dashboard():
    if session.get("pcapFilename") is None:
        return redirect('/upload')
    else:
        # load pandas dataframe
        df = pd.read_csv("./upload/temp.csv", encoding='utf-8', quotechar="'")
        # Run machine learning algorithm
        mlclass = ml.ML_Prediction()
        mlclass.load_model("model")
        prediction = mlclass.prediction("./upload/temp.binetflow")
        # Get data to plot graphs and cards
        graph_data = pcap.analysis_data_pcap(df)
        count_ip = pcap.pack_count_ip_pcap(df, 5, "src")
        return render_template('dashboard.html', ml=prediction, proto=json.dumps(graph_data[0]), tcp_flags=json.dumps(graph_data[1]),
                               total_packet=json.dumps(graph_data[2].get('Packets')), total_ip=json.dumps(graph_data[3].get('Unique_IP')),
                               packetc_ip=count_ip)


@app.route('/dashboard', methods=["POST"])
def countip():
    # Response to AJAX function for CountByIp_filter.js
    df = pd.read_csv("./upload/temp.csv", encoding='utf-8', quotechar="'")
    top = request.form.get('packetc_ip')
    loc = request.form.get('loc')
    data = pcap.pack_count_ip_pcap(df, int(top), loc)
    return data


# Route for timeline page
@app.route('/timeline')
def timeline():
    if session.get("pcapFilename") is None:
        return redirect('/upload')
    else:
        df = pd.read_csv("./upload/temp.csv", encoding='utf-8', quotechar="'")
        timeline_data = pcap.ip_interval(df, "0.0.0.0")
        # Get combined list of all unique src and dst IP addresses
        src, dst = pcap.comb_ip_pcap(df)
        list_ip = list(set(src + dst))
        list_ip.sort()

        return render_template('timeline.html', packet_time=json.dumps(timeline_data), ip_list=list_ip)


@app.route('/timeline', methods=["POST"])
def packetipfilter():
    # Response to AJAX function for timeline_filter.js
    df = pd.read_csv("./upload/temp.csv", encoding='utf-8', quotechar="'")
    tip = request.form.get('packet_time')
    data = pcap.ip_interval(df, tip)
    return data


# Route to view all pcap file raw data
@app.route('/pcap')
def pcapdata():
    if session.get("pcapFilename") is None:
        return redirect('/upload')
    else:
        df = pd.read_csv("./upload/temp.csv", encoding='utf-8', quotechar="'")
        table_data = pcap.table_pcap(df)
        return render_template('pcap_data.html', pcapdata=table_data)


@app.route('/portcomm')
def portcomm():
    if session.get("pcapFilename") is None:
        return redirect('/upload')
    else:
        df = pd.read_csv("./upload/temp.csv", encoding='utf-8', quotechar="'")
        heatmap_data = LoadData.extract_data("./upload/temp.binetflow", "192.168.10.10", "172.16.1.2", 50, "byte")
        src, dst = pcap.comb_ip_pcap(df)
        return render_template('communication_visualization.html', port_count=json.dumps(heatmap_data), srcip_list=src,
                               dstip_list=dst)


@app.route('/portcomm', methods=["POST"])
def heatmapdata():
    # Response to AJAX function for heatmap_form.js
    src_ip = str(request.form.get('srcip'))
    dst_ip = str(request.form.get('dstip'))
    data_filter = request.form.get('filterdata')
    heatmap_data = LoadData.extract_data("./upload/temp.binetflow", src_ip, dst_ip, 50, data_filter)
    return json.dumps(heatmap_data)


# Route to view all auth log raw data
@app.route('/authlog')
def authlog():
    if session.get("authFilename") is None:
        return redirect('/dashboard')
    else:
        # Change file
        log_data, col = logs.authlog(session['authFilename'])
        return render_template('auth_logs.html', col=col, logdata=log_data)


# Route to view all hist log raw data
@app.route('/histlog')
def histlog():
    if session.get("histFilename") is None:
        return redirect('/dashboard')
    else:
        log_data, col = logs.histlog(session['histFilename'])
        return render_template('hist_logs.html', col=col, logdata=log_data)
