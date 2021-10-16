import pandas as pd

'''
1. Packet count by protocol (HTTP, FTP, ...) - pie chart -- done
2. Packet count by TCP flag (SYN, ACK, ...) - pie chart -- done
3. Packet count by time, 10 min interval - bar chart -- done
4. Packet count by src IP address - bar chart -- done
5. Packet count by dst IP address - bar chart -- done
6. Total number of packet - card -- done
7. Total number of unique IP addresses - card -- done
8. src unique IP addresses
9. dst unique IP addresses
10. Number of unique packet length [added by eugene] - pie chart -- done

'''

def pcap(filname):
    analysis_list=[]
    df = pd.read_csv (filname,encoding= 'utf-8',quotechar="'", parse_dates=[0])
    
    proto_counts = df["_ws.col.Protocol"].value_counts() # Number of protocol

    tcp_flag_counts = df["tcp.flags"].value_counts() # Number of tcp flags

    interval_count = df.resample('10Min', on='frame.time').agg({'frame.time': 'count'}).rename_axis('time') # Interval of ip addr

    ip_src_counts = df["ip.src"].value_counts() # Number of src ip addr
    ip_dst_counts = df["ip.dst"].value_counts() # Number of dst ip addr

    total_packet = len(df.index) # Total number of packet
    
    unique_src = df['ip.src'].nunique() # Unique src ip addr
    unique_dst = df['ip.dst'].nunique() # Unique dst ip addr
    df["combine_ip"] = df['ip.src'].append(df['ip.dst'],ignore_index=True) # Combine both src and dst to a single df
    unique_combine = df["combine_ip"].nunique() # Unique combine ip addr

    pkt_length_counts = df["_ws.col.Length"].value_counts() # Number of packet length

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

    ip_src_counts_dict = ip_src_counts.reset_index()
    ip_src_counts_dict.columns =['Src_IP_Addr','IP_Addr_Count']
    analysis_list.append(ip_src_counts_dict.to_dict('records'))

    ip_dst_counts_dict = ip_dst_counts.reset_index()
    ip_dst_counts_dict.columns =['Dst_IP_Addr','IP_Addr_Count']
    analysis_list.append(ip_dst_counts_dict.to_dict('records'))

    total_packet_dict = [{"Packets":total_packet}]
    analysis_list.append(total_packet_dict)

    unique_combine_dict = [{"Unique_IP":unique_combine}]
    analysis_list.append(unique_combine_dict)

    ip_src_counts_dict = ip_src_counts.reset_index()
    ip_src_counts_dict.columns =['Src_IP_Addr','IP_Addr_Count']
    analysis_list.append(ip_src_counts_dict.to_dict('records'))

    # unique_src_dict = unique_src.reset_index()
    # unique_src_dict.columns =['Unique_Src_IP_Addr','IP_Addr_Count']
    # analysis_list.append(unique_src_dict.to_dict('records'))
    #
    # unique_dst_dict = unique_dst.reset_index()
    # unique_dst_dict.columns =['Unique_Dst_IP_Addr','IP_Addr_Count']
    # analysis_list.append(unique_dst_dict.to_dict('records'))

    pkt_length_counts_dict = pkt_length_counts.reset_index()
    pkt_length_counts_dict.columns =['Packets_Length','Packets_Length_Count']
    analysis_list.append(pkt_length_counts_dict.to_dict('records'))

    return analysis_list, table_dict

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