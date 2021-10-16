import json
from os import system

import logs
import LoadData
import ml

from flask import Flask, render_template, redirect, request

app = Flask(__name__)


# Route for default page
@app.route('/', methods=["POST", "GET"])
def home():
    return redirect('/dashboard')


# Route for dashboard page
@app.route('/dashboard')
def dashboard():
    test_ip = {'192.10.3.2': "10", '172.10.3.2': "500", "172.10.3.1": "232", "172.10.5.1":"324"}
    bubble_data = LoadData.extract_data("./upload/secure-server.binetflow", "192.168.10.10", "172.16.1.2", 50, "byte")
    mlclass = ml.ML_Prediction()
    mlclass.load_model("model")
    prediction = mlclass.prediction("./upload/secure-server.binetflow")
    return render_template('dashboard.html', ip=test_ip, port_count=json.dumps(bubble_data), ml=prediction)


@app.route('/dashboard', methods=["POST"])
def heatmapdata():
    src_ip = str(request.form.get('srcip'))
    dst_ip = request.form.get('dstip')
    data_filter = request.form.get('filterdata')
    bubble_data = LoadData.extract_data("./upload/secure-server.binetflow", src_ip, dst_ip, 50, data_filter)
    return json.dumps(bubble_data)


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
    pcap_file = request.files['pcap']
    log_file = request.files['file']
    log_file2 = request.files['file2']
    
    print("hello")
    # pcap save
    if pcap_file.filename != '':
        
        pcap_file.save("upload/"+pcap_file.filename)

        # require tshark
        # require argus-server
        # saved in a folder called upload(change name if needs be) 
        system("tshark -r upload/" + pcap_file.filename + " -T fields -E header=y -E separator=, -E occurrence=a -E quote=s" 
        " -e frame.time -e _ws.col.Protocol -e _ws.col.Length -e tcp.flags -e ip.src -e tcp.srcport -e udp.srcport -e ip.dst" 
        " -e tcp.dstport -e udp.dstport -e _ws.col.Info > upload/temp.csv")

        #precreate an empty asd.biargus file, idk why also, but kk say do it
        system("argus -F utils/argus.conf -r upload/" + pcap_file.filename + " -w temp.biargus | ra -r temp.biargus -n -F utils/ra.conf -Z b > upload/temp.binetflow")

    # log file 1 save
    print(log_file.filename)
    if log_file.filename != '':
        log_file.save("upload/"+log_file.filename)

    # log file 2 save
    if log_file2.filename != '':
        log_file2.save("upload/"+log_file2.filename)

    return render_template('upload.html')

'''
<form action = "/json" method = "POST" enctype = "multipart/form-data">
    <input type = "file" name = "pcap" />
    <input type = "file" name = "file" />
    <input type = "file" name = "file2" />
    <input type = "submit"/>
</form>
'''
