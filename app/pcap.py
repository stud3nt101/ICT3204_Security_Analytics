import pandas as pd
from pandas.core.series import Series

'''
Converts PCAP file into processable data
*Timezone is in PDT

Function 1: Raw PCAP table data
Function 2: All unique source & dest ip
Function 3: Packet count by IP
    - Takes in filename, top 5/10/15, src/dst
Function 4: Occurace of a single ip address every 10 min
    - Takes in a single ip address as an input and returns the number of occurace every 10 min 
Function 5: List of dictionary in the following index order.
    0. Packet count by protocol (HTTP, FTP, ...)
    1. Packet count by TCP flag (SYN, ACK, ...)
    2. Packet count by time, in 10 min interval
    3. Total number of packets
    4. Total number of unique IP addresses
'''


# table data
def table_pcap(df) -> dict:
    table_dict = df.to_dict('records')
    
    return table_dict


# src unique IP addresses & dst unique IP addresses
def comb_ip_pcap(df) -> list:
    srcip_list = df['ip.src'].unique()
    dstip_list = df['ip.dst'].unique()

    # Clean list of unique src IP
    srcip_cleaned = [x for x in srcip_list if str(x) != 'nan'] # Remove nan
    srcip_cleaned.sort()

    # Clean list of unique dst IP
    dstip_cleaned = [x for x in dstip_list if str(x) != 'nan'] # Remove nan
    dstip_cleaned.sort()

    return srcip_cleaned, dstip_cleaned


# Packet count by IP address
def pack_count_ip_pcap(df, top, loc) -> dict:
    
    if loc == "src":
        ip_counts = df["ip.src"].value_counts().head(top)
    else:
        ip_counts = df["ip.dst"].value_counts().head(top)
    
    dict_ipcount = dict(ip_counts)
    
    for key in dict_ipcount:
        dict_ipcount[key] = int(dict_ipcount[key])
    
    return dict_ipcount

# Occurace of a single ip address every 10 min
def ip_interval(df, ip_addr) -> dict:
    # Creating the correct datetime formate for processing
    df['frame.time'] = df['frame.time'].str.replace('PDT','').str.strip()
    df['frame.time'] = pd.to_datetime(df['frame.time'], format='%b %d, %Y %H:%M:%S.%f')
    
    # Recreating a new dataframe to store combine ip address of src & dst
    frame_time_df = df['frame.time'].append(df['frame.time'], ignore_index=True)
    comb_ip_df = df['ip.src'].append(df['ip.dst'], ignore_index=True)
    time_ip_df = pd.concat([frame_time_df, comb_ip_df], axis=1, keys=['Time','Combine_IP'])

    # Locating the desired ip address
    found_ip = time_ip_df.loc[time_ip_df['Combine_IP']==ip_addr]
    
    # Group and couting based on the 10 min interval
    interval_count = found_ip.resample('10Min', on='Time').agg({'Combine_IP': 'count'})
    interval_count_df = interval_count.reset_index()
    interval_count_df.columns = ['Time','Count']
    interval_count_df['Time'] = interval_count_df['Time'].dt.strftime('%Y-%m-%d %r')
    interval_count_dict = dict(interval_count_df.values)

    return interval_count_dict

def analysis_data_pcap(df) -> dict:
    analysis_data_list = []

    # Number of protocol
    proto_counts = df["_ws.col.Protocol"].value_counts() 
    proto_counts_dict = proto_counts.reset_index()
    proto_counts_dict.columns = ['Protocol', 'Protocol_Count']
    analysis_data_list.append(dict(proto_counts_dict.values))
    
    # Number of tcp flags
    tcp_flag_counts = df["tcp.flags"].value_counts() 
    tcp_flag_dict = tcp_flag_counts.reset_index()
    tcp_flag_dict.columns = ['TCP_Flags','TCP_Flags_Count']
    analysis_data_list.append(dict(tcp_flag_dict.values))

    # Total number of packet
    total_packet = len(df.index) 
    total_packet_dict = {"Packets":total_packet}
    analysis_data_list.append(total_packet_dict)
    
    # Unique combine ip addr
    comb_ip = df['ip.src'].append(df['ip.dst'], ignore_index=True)
    unique_comb = comb_ip.dropna().nunique()
    unique_comb_dict = {"Unique_IP":unique_comb}
    analysis_data_list.append(unique_comb_dict)

    return analysis_data_list