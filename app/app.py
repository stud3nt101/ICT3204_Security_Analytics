import json
import os
from os import system

from pandas.io.parsers import TextParser

import logs
import LoadData, ml
import pcap

from flask import Flask, render_template, redirect, request

app = Flask(__name__)

temp_file = []

ALLOWED_EXTENSIONS = set(['pcapng','log'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for default page
@app.route('/', methods=["POST", "GET"])
def home():
    return redirect('/dashboard')


# Route for dashboard page
@app.route('/dashboard')
def dashboard():
    mlclass = ml.ML_Prediction()
    mlclass.load_model("model")
    prediction = mlclass.prediction("./upload/temp.binetflow")
    graph_data, table_data = pcap.pcap_analysis("./upload/temp.csv")
    return render_template('dashboard.html', ml=prediction, ip=json.dumps(graph_data[1]),
                           proto=json.dumps(graph_data[0]), total_packet=json.dumps(graph_data[5].get('Packets')),
                           total_ip=json.dumps(graph_data[6].get('Unique_IP')), packet_srcip=json.dumps(graph_data[3]),
                           packet_dstip=json.dumps(graph_data[4]), packet_time=json.dumps(graph_data[2]))


@app.route('/pcap')
def pcapdata():
    graph_data, table_data = pcap.pcap_analysis("./upload/temp.csv")
    return render_template('pcap_data.html', pcapdata=table_data)


@app.route('/portcomm')
def portcomm():
    heatmap_data = LoadData.extract_data("./upload/temp.binetflow", "192.168.10.10", "172.16.1.2", 50, "byte")
    graph_data, table_data = pcap.pcap_analysis("./upload/temp.csv")
    return render_template('communication_visualization.html', port_count=json.dumps(heatmap_data), srcip_list=json.dumps(graph_data[7]),
                           dstip_list=json.dumps(graph_data[8]))


@app.route('/portcomm', methods=["POST"])
def heatmapdata():
    src_ip = str(request.form.get('srcip'))
    dst_ip = request.form.get('dstip')
    data_filter = request.form.get('filterdata')
    heatmap_data = LoadData.extract_data("./upload/temp.binetflow", src_ip, dst_ip, 50, data_filter)
    return json.dumps(heatmap_data)


@app.route('/authlog')
def authlog():
    # Change file
    log_data, col = logs.authlog("./Logs/auth.log")
    return render_template('auth_logs.html', col=col, logdata=log_data)


@app.route('/histlog')
def histlog():
    log_data, col = logs.histlog("./Logs/hist.log")
    return render_template('hist_logs.html', col=col, logdata=log_data)

@app.route('/upload-process', methods=["POST","GET"])
def upload_process():
    data = request.files['file']
    path = "Logs/"
    files = os.listdir(path)
    print(files)
    if allowed_file(data.filename) and len(temp_file) < 3:
        temp_file.append(data)
        if data.filename.rsplit('.', 1)[1].lower() == "log":
            if len(files) == 0:
                data.save("Logs/auth.log")
            else:
                data.save("Logs/hist.log")
        else:
            data.save("upload/"+data.filename)
        return render_template('upload.html')
    else:
        return redirect('upload.html')

# Route for upload page
@app.route('/upload-complete', methods=["POST","GET"])
def upload_complete():
    check = None
    path = "upload/"
    files = os.listdir(path)

    try:
        if len(temp_file) != 0:
            for filename in files:
                for fileobject in temp_file:
                    if fileobject.filename != filename:
                        os.remove(path+filename)
    except:
        pass

    for file in temp_file:
        if file.filename.rsplit('.', 1)[1].lower() == "pcapng":
            check = 1
            break
            
    if len(temp_file) != 0 and check != None:
        for file in temp_file:
            if file.filename.rsplit('.', 1)[1].lower() == "pcapng":


                # require tshark
                # require argus-server
                # saved in a folder called upload(change name if needs be) 
                system("tshark -r upload/" + file.filename + " -T fields -E header=y -E separator=, -E occurrence=a -E quote=s" 
                " -e frame.time -e _ws.col.Protocol -e _ws.col.Length -e tcp.flags -e ip.src -e tcp.srcport -e udp.srcport -e ip.dst" 
                " -e tcp.dstport -e udp.dstport -e _ws.col.Info > upload/temp.csv")

                #precreate an empty asd.biargus file, idk why also, but kk say do it
                system("argus -F utils/argus.conf -r upload/" + file.filename + " -w temp.biargus | ra -r temp.biargus -n -F utils/ra.conf -Z b > upload/temp.binetflow")

        temp_file.clear()
        return redirect('/dashboard')
    else:
        temp_file.clear()
        return render_template('upload.html')

# Route for upload page
@app.route('/upload', methods=["POST","GET"])
def upload():

    return render_template('upload.html')
    pcap_file = request.files['pcap']
    log_file = request.files['file']
    log_file2 = request.files['file2']

    

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
