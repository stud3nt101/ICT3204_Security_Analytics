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

timezone is in PDT
Split pcap.py into at least 5 functions (can be more if its easier for you, doesn't matter. Just need at least function 1-4):

The pandas read function     
df = pd.read_csv (filname,encoding= 'utf-8',quotechar="'")

function 1: table data
function 2: All unique source & dest ip (Point 8 & 9)
   - List of each unique IP ["10.0.0.0", "0.0.0.0"]
function 3: Packet count by src ip (Point 4)
   - Take in filename & 5/10/15 (or whichever is best for u)
function 4: Packet count by dst ip (Point 5) 
   - Take in filename & 5/10/15 (or whichever is best for u)
function 5: the rest of the data (Point 1-3, 6, 7, 10)
'''

# table data
def table_pcap(filname) -> dict:
    table_dict = df.to_dict('records')
    
    return table_dict

# src unique IP addresses & dst unique IP addresses [combine] (point 8 & 9)
def comb_ip_pcap(filname) -> list:  
    comb_ip = df['ip.src'].append(df['ip.dst'], ignore_index=True) # Combine both src and dst to a single df
    comb_ip_list = combine_ip.dropna().unique()
    
    return combine_ip_list

#  Packet count by dst IP address (point 5)
def pack_count_src_pcap(filname) -> dict:
    ip_src_counts_top15 = df["ip.src"].value_counts().head(15)
    
    return dict(ip_src_counts_top15)

# Packet count by src IP address (point 4)
def pack_count_dst_pcap(filname) -> dict:
    ip_dst_counts_top15 = df["ip.dst"].value_counts().head(15)

    return dict(ip_dst_counts_top15)

# All the other stuffs
def analysis_data_pcap(filname) -> [dict]:
    analysis_data_list = []
    
    # Number of protocol (point 1)
    proto_counts = df["_ws.col.Protocol"].value_counts() 
    proto_counts_dict = proto_counts.reset_index()
    proto_counts_dict.columns = ['Protocol','Protocol_Count']
    analysis_data_list.append(dict(proto_counts_dict.values))
    
    # Number of tcp flags (point 2)
    tcp_flag_counts = df["tcp.flags"].value_counts() 
    tcp_flag_dict = tcp_flag_counts.reset_index()
    tcp_flag_dict.columns = ['TCP_Flags','TCP_Flags_Count']
    analysis_data_list.append(dict(tcp_flag_dict.values))

    # 10 min interval on ip addr (point 3)
    df['frame.time'] = df['frame.time'].str.replace('PDT','').str.strip()
    df['frame.time'] = pd.to_datetime(df['frame.time'], format='%b %d, %Y %H:%M:%S.%f')
    interval_count = df.resample('10Min', on='frame.time').agg({'frame.time': 'count'}).rename_axis('time') 
    interval_count_dict = interval_count.reset_index()
    interval_count_dict.columns = ['Time','Time_Count']
    interval_count_dict['Time'] = interval_count_dict['Time'].dt.strftime('%Y-%m-%d %r')
    analysis_data_list.append(dict(interval_count_dict.values))

    # Total number of packet (point 6)
    total_packet = len(df.index) 
    total_packet_dict = {"Packets":total_packet}
    analysis_data_list.append(total_packet_dict)
    
    # Unique combine ip addr (point 7)
    comb_ip = df['ip.src'].append(df['ip.dst'], ignore_index=True)
    unique_comb = comb_ip.dropna().nunique()
    unique_comb_dict = {"Unique_IP":unique_comb}
    analysis_data_list.append(unique_comb_dict)

    # Number of packet length (point 10)
    pkt_length_counts = df["_ws.col.Length"].value_counts() 
    pkt_length_counts_dict = pkt_length_counts.reset_index()
    pkt_length_counts_dict.columns = ['Packets_Length','Packets_Length_Count']
    analysis_data_list.append(dict(pkt_length_counts_dict.values))

    return analysis_data_list

# idk who wrote this, but i will just leave this here in case -- eugene
# try:
#     pcap_analysis('upload/temp.csv')
# except:
#     pass