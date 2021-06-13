import json
import gzip
import os 
import sys
import matplotlib.pyplot as plt
import numpy as np
from datetime import date
import datetime



def draw_graph():
    # date -----------------------------------
    today = date.today()

    now = datetime.datetime.now()
    nowDate = str(now.strftime('%Y-%m-%d'))
    nowTime = str(now.strftime('%H'))

    # path -----------------------------------
    path = './cwEC2logtest_networkout_web2.txt'

    # read -----------------------------------
    with open(path,'r') as j_file : 
        net_json_data = json.load(j_file)
        print(type(net_json_data), '\n\n') ## dic type

    net_json_data2 = net_json_data['Datapoints']

    net_time_data = []
    net_max_data = []

    for i in range(len(net_json_data2)):
        net_time_data.append(net_json_data2[i]['Timestamp'])
        net_max_data.append(net_json_data2[i]['Maximum'])

    # time - hh
    net2_time_data2 = []

    for i in range(len(net_time_data)):
        Z_NUM = net_time_data[0].find('T') + 1
        Z_NUM2 = Z_NUM + 2
        net_time_data2_split_t = net_time_data[i][Z_NUM:Z_NUM2] 
        net2_time_data2.append(int(net_time_data2_split_t))

    # graph
    plt.bar(net2_time_data2 ,net_max_data,width=0.7,color = 'green')
    plt.xlabel('TIME')
    plt.ylabel("NET-MAX")
    plt.title('WEB2_NET-MAX_GRAPH')
    plt.savefig('./{0}-{1}_WEB2_NET_MAX_graph.png'.format(nowDate,nowTime),dpi=300)
    # plt.show()