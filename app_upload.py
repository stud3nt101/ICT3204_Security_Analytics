from flask import Flask, render_template, request
from os import listdir, system
import pandas as pd
import json

# total number of packet
# Number of packet by protocol
# Number of total packet per interval (10)


app = Flask(__name__)

def get_users(offset, per_page, data):

    return data[offset: offset + per_page]

@app.route("/")
def home():
    fileList = listdir("upload")
    return render_template("upload.html",test=fileList)

@app.route('/json', methods=['POST'])
def upload_file():
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
        system("tshark -r upload/" + pcap_file.filename + " -T fields -E header=y -E separator=, -E occurrence=a -E quote=d" 
        " -e frame.time -e _ws.col.Protocol -e _ws.col.Length -e tcp.flags -e ip.src -e tcp.srcport -e udp.srcport -e ip.dst" 
        " -e tcp.dstport -e udp.dstport -e _ws.col.Info > upload/test.csv")

        #precreate an empty asd.biargus file, idk why also, but kk say do it
        system("argus -F utils/argus.conf -r upload/" + pcap_file.filename + "  -w asd.biargus | ra -r asd.biargus -n -F utils/ra.conf -Z b > upload/file.binetflow")

    # log file 1 save
    print(log_file.filename)
    if log_file.filename != '':
        log_file.save("upload/"+log_file.filename)

    # log file 2 save
    if log_file2.filename != '':
        log_file2.save("upload/"+log_file2.filename)

    return render_template('json.html')

if __name__ == "__main__":
    app.run(debug=True)