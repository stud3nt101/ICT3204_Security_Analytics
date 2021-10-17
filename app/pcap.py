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

def pcap_analysis(filname):
    analysis_list=[]
    df = pd.read_csv (filname,encoding= 'utf-8',quotechar="'", parse_dates=[0])

    proto_counts = df["_ws.col.Protocol"].value_counts() # Number of protocol

    tcp_flag_counts = df["tcp.flags"].value_counts() # Number of tcp flags

    interval_count = df.resample('10Min', on='frame.time').agg({'frame.time': 'count'}).rename_axis('time') # Interval of ip addr

    # Converting main df to dict to be outputted into pagination table
    df['frame.time']=df['frame.time'].dt.strftime('%Y-%m-%d %r')
    table_dict = df.to_dict('records')

    ip_src_counts = df["ip.src"].value_counts() # Number of src ip addr
    ip_dst_counts = df["ip.dst"].value_counts() # Number of dst ip addr

    total_packet = len(df.index) # Total number of packet
    
    unique_src = df['ip.src'].nunique() # Unique src ip addr
    unique_dst = df['ip.dst'].nunique() # Unique dst ip addr
    df["combine_ip"] = df['ip.src'].append(df['ip.dst'],ignore_index=True) # Combine both src and dst to a single df
    unique_combine = df["combine_ip"].nunique() # Unique combine ip addr

    pkt_length_counts = df["_ws.col.Length"].value_counts() # Number of packet length

    # Preping the respective df to be converted to dict 
    # datastructure --> [{key1:value1, key2:value2}, {key3:value3, key4:value4}]
    proto_counts_dict = proto_counts.reset_index()
    proto_counts_dict.columns = ['Protocol','Protocol_Count']
    analysis_list.append(dict(proto_counts_dict.values))

    tcp_flag_dict = tcp_flag_counts.reset_index()
    tcp_flag_dict.columns = ['TCP_Flags','TCP_Flags_Count']
    analysis_list.append(dict(tcp_flag_dict.values))

    interval_count_dict = interval_count.reset_index()
    interval_count_dict.columns =['Time','Time_Count']
    interval_count_dict['Time']=interval_count_dict['Time'].dt.strftime('%Y-%m-%d %r')
    analysis_list.append(dict(interval_count_dict.values))

    ip_src_counts_dict = ip_src_counts.reset_index()
    ip_src_counts_dict.columns =['Src_IP_Addr','IP_Addr_Count']
    analysis_list.append(dict(ip_src_counts_dict.values))

    ip_dst_counts_dict = ip_dst_counts.reset_index()
    ip_dst_counts_dict.columns =['Dst_IP_Addr','IP_Addr_Count']
    analysis_list.append(dict(ip_dst_counts_dict.values))

    total_packet_dict = {"Packets":total_packet}
    analysis_list.append(total_packet_dict)

    unique_combine_dict = {"Unique_IP":unique_combine}
    analysis_list.append(unique_combine_dict)

    ip_src_counts_dict = ip_src_counts.reset_index()
    ip_src_counts_dict.columns =['Src_IP_Addr','IP_Addr_Count']
    analysis_list.append(dict(ip_src_counts_dict.values))

    unique_src_dict = {"Unique_Src_IP":unique_src}
    analysis_list.append(unique_src_dict)

    unique_dst_dict = {"Unique_Dst_IP":unique_dst}
    analysis_list.append(unique_dst_dict)

    pkt_length_counts_dict = pkt_length_counts.reset_index()
    pkt_length_counts_dict.columns =['Packets_Length','Packets_Length_Count']
    analysis_list.append(dict(pkt_length_counts_dict.values))

    return analysis_list, table_dict