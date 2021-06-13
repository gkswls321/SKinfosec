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



    # path ----------------------------------------
    # cbs-log-combine.py 에서 합친 로그파일들 중 web1 과 web2 의 동일 종류 로그를 합친다.
    f_inputpath1 = "./tmp_web1-mysql-error-log_combine.txt"
    f_inputpath2 = "./tmp_web2-mysql-error-log_combine.txt"
    f_outpath_combined = "./tmp_weball-mysql-error-log_allcombine.txt"
    with open(f_inputpath1, 'r') as f_input1:
        f_read1 = f_input1.readlines()
        with open(f_inputpath2, 'r') as f_input2:
            f_read2 = f_input2.readlines()
            with open(f_outpath_combined, "w+") as f_out_combined:
                for line in f_read1:
                    f_out_combined.write(line)
                for line in f_read2:
                    f_out_combined.write(line)

    f_out_combined.close()
    f_input2.close()
    f_input1.close()



    mysql_path = f_outpath_combined

    # read ------------------------------------------------------
    mysql_r = open(mysql_path,'r')
    mysql_r_data = mysql_r.readlines()

    mysql_split = []
    for line in mysql_r_data: 
        mysql_split.append(line)

    # for line in mysql_split:
    #     print(line)

    mysql_Warning = [] # warning list
    mysql_Note = [] # Note list
    mysql_error_t = [] # time list
    mysql_list_d_t = [] # time list -> int

    # warning -------------------------- 
    mysql_Warning2 = []

    for i in range(len(mysql_split)):
        if '[Warning]' in mysql_split[i]:
            mysql_Warning2.append(mysql_split[i])

    for i in range(len(mysql_split)):
        Z_Warning = mysql_split[i].find('[Warning]') 
        mysql_split_warning = mysql_split[i][Z_Warning:]
        if mysql_split_warning.startswith('[') : 
            mysql_Warning.append(mysql_split_warning)

    for line in mysql_Warning:
        print(line)

    # note --------------------------------
    for i in range(len(mysql_split)):
        if '[Note]' in mysql_split[i]:
            mysql_Note.append(mysql_split[i])

    # time -----------------------------
    print('time_LOG START!','\n\n') 

    for i in range(len(mysql_split)):
        data = mysql_split[i][36:52]
        if data.endswith('Z'): 
            data = data[:2]
            # print(data)
            mysql_error_t.append(int(data))

    tm_00 = 0
    tm_02 = 0
    tm_04 = 0
    tm_06 = 0
    tm_08 = 0
    tm_10 = 0
    tm_12 = 0
    tm_14 = 0
    tm_16 = 0
    tm_18 = 0
    tm_20 = 0
    tm_22 = 0

    for i in range(len(mysql_error_t)):
        time_data = mysql_error_t[i]
        if time_data >= 22:
            tm_22 += 1
        elif time_data >= 20:
            tm_20 += 1 
        elif time_data >= 18:
            tm_18 += 1 
        elif time_data >= 16:
            tm_16 += 1 
        elif time_data >= 14:
            tm_14 += 1 
        elif time_data >= 12:
            tm_12 += 1         
        elif time_data >= 10:
            tm_10 += 1 
        elif time_data >= 8:
            tm_08 += 1   
        elif time_data >= 6:
            tm_06 += 1   
        elif time_data >= 4:
            tm_04 += 1   
        elif time_data >= 2:
            tm_02 += 1         
        elif time_data >= 0:
            tm_00 += 1
        else :
            break

    tm_x_values = ['00','02','04','06','08','10','12','14','16','18','20','22']
    ap_values = [tm_00 , tm_02, tm_04, tm_06, tm_08, tm_10, tm_12, tm_14, tm_16, tm_18, tm_20, tm_22]
    plt.subplot(121)
    plt.scatter(tm_x_values,ap_values, c = 'b', s = 40)
    plt.plot(tm_x_values,ap_values,linestyle='solid',color='green')
    plt.title('MYSQl_TIME', fontsize=20)
    plt.xlabel('time',fontsize=15)
    plt.ylabel('count',fontsize=10)

    plt.savefig('./{0}-{1}_mysql_error_graph.png'.format(nowDate,nowTime),dpi=300)


    # GRAPH
    mysql_x_1 = ['[Note]','[Warning]']
    mysql_y_1 = [len(mysql_Note), len(mysql_Warning)]
    plt.subplot(122)
    plt.bar(mysql_x_1 ,mysql_y_1,width=0.7,color = 'green')
    plt.xlabel('Type')
    plt.ylabel('Count')
    plt.title('MYSQL_ERROR_TYPE_graph')
    plt.savefig('./{0}-{1}_MYSQL_ERROR_TYPE_graph.png'.format(nowDate,nowTime),dpi=300)
    # plt.show()
