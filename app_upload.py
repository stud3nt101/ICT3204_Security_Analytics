from flask import Flask, render_template, request
from os import listdir, system
import pandas as pd
import json

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

    return render_template('json.html')


'''
1. Packet count by protocol (HTTP, FTP, ...) - pie chart -- done
2. Packet count by TCP flag (SYN, ACK, ...) - pie chart -- done
3. Packet count by time, 10 min interval - bar chart -- done
4. Packet count by IP address - bar chart -- done (The total number of unique ip =/= the total number of packet some packet do not have ip address (i guess is intended??))
5. Total number of packet - card -- done
6. Total number of unique IP addresses - card -- done
7. Number of unique packet length [added by eugene] - pie chart -- done

@Claudia I have included both the % and number count variant, pick and choose whichever fits your case better (default is count and not %)
'''


@app.route('/display2', methods=['GET', 'POST'])
def display2():
    
    analysis_list=[]
    df = pd.read_csv ('upload/testing.csv',encoding= 'utf-8',quotechar="'", parse_dates=[0])

    df["combine_ip"] = df['ip.src'].append(df['ip.dst'],ignore_index=True) # Combine both src and dst to a single df
    
    proto_counts = df["_ws.col.Protocol"].value_counts() # Number of protocol
    proto_percent = df["_ws.col.Protocol"].value_counts(normalize=True) # % of protocol distribution

    tcp_flag_counts = df["tcp.flags"].value_counts() # Number of tcp flags
    tcp_flag_percent = df["tcp.flags"].value_counts(normalize=True) # % of tcp flags distribution

    interval_count = df.resample('10Min', on='frame.time').agg({'frame.time': 'count'}).rename_axis('time')

    ip_src_counts = df["ip.src"].value_counts() # Number of src ip addr
    ip_src_percent = df["ip.src"].value_counts(normalize=True) # % of src ip addr distribution
    ip_dst_counts = df["ip.dst"].value_counts() # Number of dst ip addr
    ip_dst_percent = df["ip.dst"].value_counts(normalize=True) # % of dst ip addr distribution
    ip_combine_counts = df["combine_ip"].value_counts() # Number of combine ip addr
    ip_combine_percent = df["combine_ip"].value_counts(normalize=True) # % of combine ip addr distribution

    total_packet = len(df.index) # Total number of packet
    
    unique_src = df['ip.src'].nunique() # Unique src ip addr
    unique_dst = df['ip.dst'].nunique() # Unique dst ip addr
    unique_combine = df["combine_ip"].nunique() # Unique combine ip addr

    pkt_length_counts = df["_ws.col.Length"].value_counts() # Number of packet length
    pkt_length_percent = df["_ws.col.Length"].value_counts(normalize=True) # % of packet length distribution

    # Converting main df to dict to be outputted into pagination table
    table_dict = df.to_dict('records')

    # Preping the respective df to be converted to dict 
    # datastructure --> [[{column1:data1, column2:data2}]] (refer to sample html code below for sample usage)
    proto_counts_dict = proto_counts.reset_index()
    proto_counts_dict.columns = ['Protocol','Protocol_Count']
    analysis_list.append(proto_counts_dict.to_dict('records'))
    
    tcp_flag_dict = tcp_flag_counts.reset_index()
    tcp_flag_dict.columns = ['TCP_Flags','TCP_Flags_Count']
    analysis_list.append(tcp_flag_dict.to_dict('records'))

    interval_count_dict = interval_count.reset_index()
    interval_count_dict.columns =['Time','Time_Count']
    analysis_list.append(interval_count_dict.to_dict('records'))

    ip_combine_counts_dict = ip_combine_counts.reset_index()
    ip_combine_counts_dict.columns =['IP_Addr','IP_Addr_Count']
    analysis_list.append(ip_combine_counts_dict.to_dict('records'))

    total_packet_dict = [{"Packets":total_packet}]
    analysis_list.append(total_packet_dict)

    unique_combine_dict = [{"Unique_IP":unique_combine}]
    analysis_list.append(unique_combine_dict)

    pkt_length_counts_dict = pkt_length_counts.reset_index()
    pkt_length_counts_dict.columns =['Packets_Length','Packets_Length_Count']
    analysis_list.append(pkt_length_counts_dict.to_dict('records'))

    return render_template('json.html', ctrsuccess=analysis_list, table=table_dict)

if __name__ == "__main__":
    app.run(debug=True)

'''
------------------
Sample html usage|
-----------------

{%if ctrsuccess %}
<div class="table-responsive">
    <table class="table table-striped">
        <tbody>
            <h1>Protocol</h1>
            {% for dict_item in ctrsuccess[0]%}
                
                </tr>
                    <td>{{ dict_item['Protocol'] }} : {{ dict_item['Protocol_Count'] }}</td>
                </tr>
               
            {% endfor %}
        </tbody>
    </table>
    <table>
        <tbody>
            <h1>TCP_FLag</h1>
            {% for x in ctrsuccess[1]%}
                
                </tr>
                    <td>{{ x['TCP_Flags'] }} : {{ x['TCP_Flags_Count'] }}</td>
                </tr>
               
            {% endfor %}
        </tbody>
    </table>
    <table>
        <tbody>
            <h1>Interval</h1>
            {% for x in ctrsuccess[2]%}
                
                </tr>
                    <td>{{ x['Time'] }} : {{ x['Time_Count'] }}</td>
                </tr>
               
            {% endfor %}
        </tbody>
    </table>
    <table>
        <tbody>
            <h1>Occurance of Unique IP Address</h1>
            {% for x in ctrsuccess[3]%}
                
                </tr>
                    <td>{{ x['IP_Addr'] }} : {{ x['IP_Addr_Count'] }}</td>
                </tr>
               
            {% endfor %}
        </tbody>
    </table>
    <table>
        <tbody>
            <h1>Total Packet</h1>
            {% for x in ctrsuccess[4]%}
                
                </tr>
                    <td>{{ x['Packets'] }}</td>
                </tr>
               
            {% endfor %}
        </tbody>
    </table>
    <table>
        <tbody>
            <h1>Total Number of unique IP</h1>
            {% for x in ctrsuccess[5]%}
                
                </tr>
                    <td>{{ x['Unique_IP'] }}</td>
                </tr>
               
            {% endfor %}
        </tbody>
    </table>
    <table>
        <tbody>
            <h1>Occurace of Packet Length</h1>
            {% for x in ctrsuccess[6]%}
                
                </tr>
                    <td>{{ x['Packets_Length'] }} : {{ x['Packets_Length_Count'] }}</td>
                </tr>
               
            {% endfor %}
        </tbody>
    </table>
    <table>
        <tbody>
            <h1>table</h1>
            {% for x in table%}
                
                </tr>
                    <td>{{ x['frame.time'] }}</td> <--- replace with relevant field name as needed (referenced from the tshark command above) 
                </tr>
               
            {% endfor %}
        </tbody>
    </table>
</div>
{%endif%}
'''