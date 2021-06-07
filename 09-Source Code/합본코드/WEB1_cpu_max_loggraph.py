import json
import gzip
import os 
import sys
import matplotlib.pyplot as plt
import numpy as np
from datetime import date
import datetime

# date -----------------------------------
today = date.today()

now = datetime.datetime.now()
nowDate = str(now.strftime('%Y-%m-%d'))
nowTime = str(now.strftime('%H'))

# path -----------------------------------
path = './cwEC2logtest_CPUmax_web1.txt'

# read -----------------------------------
with open(path,'r') as j_file : 
    cpu_json_data = json.load(j_file)
    print(type(cpu_json_data), '\n\n') ## dic type
    # print(cpu_json_data,'\n\n\n')

cpu_json_data2 = cpu_json_data['Datapoints']

cpu_time_data = []
cpu_max_data = []

for i in range(len(cpu_json_data2)):
    cpu_time_data.append(cpu_json_data2[i]['Timestamp'])
    cpu_max_data.append(cpu_json_data2[i]['Maximum'])

# time - hh
# print(len(cpu_time_data))
# print(cpu_time_data[0])

cpu_time_data2 = []

for i in range(len(cpu_time_data)):
    Z_NUM = cpu_time_data[0].find('T') + 1
    Z_NUM2 = Z_NUM + 2
    ec2_cpu_2_split_t = cpu_time_data[i][Z_NUM:Z_NUM2] 
    cpu_time_data2.append(int(ec2_cpu_2_split_t))

# GRAPH
plt.bar(cpu_time_data2 ,cpu_max_data,width=0.7,color = 'green')
plt.xlabel('TIME')
plt.ylabel("CPU-MAX")
plt.title('WEB_CPU-MAX_GRAPH')
plt.savefig('./{0}-{1}_WEB1_CPU_MAX_graph.png'.format(nowDate,nowTime),dpi=300)
# plt.show()