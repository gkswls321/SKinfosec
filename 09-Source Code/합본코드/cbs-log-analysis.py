import gzip
import os
import sys
import json
from datetime import date
# 코드 실행 예시:
# python ./cbs-log-analysis.py 년 월 일 로그타입
# python ./cbs-log-analysis.py 2021 5 31 ct-log
# python ./cbs-log-analysis.py 2021 6 3 web1-mysql-error-log
# python ./cbs-log-analysis.py 2021 6 3 web1-apache2-error-log


# dict_logtype = {
#     "ct-log" : "ct-log",      <=입력받는 로그 종류 : 해당 로그 폴더 상대경로
#     "mysql-error" : "mysql-error.log",
#     "s3lambda" : "aws-lambda-beom-cw-s3",
#     "messagelog" : "messagelog",
#     "db-error" : "aws-rds-instance-dev-db-error"
# }

# 파이썬 3버전 (3.6.8 버전)



# 'web1_mysql_error_log' = 'web1-mysql-error-log/'
# 'web1_apache2_error_log' = 'web1-apache2-error-log/'
# 'web2_mysql_error_log' = 'web2-mysql-error-log/'
# 'web2_apache2_error_log' = 'web2-apache2-error-log/'


# 'web1-mysql-error-log' : 'web1-mysql-error-log',
# 'web1-apache2-error-log' : 'web1-apache2-error-log',
# 'web2-mysql-error-log' : 'web2-mysql-error-log',
# 'web2-apache2-error-log' : 'web2-apache2-error-log'




dict_logtype = {
    # "ct-log" : "ct-log",
    # "mysql-error" : "mysql-error.log",
    # "s3lambda" : "aws-lambda-beom-cw-s3",
    # "messagelog" : "messagelog",
    # "db-error" : "aws-rds-instance-dev-db-error",
    'web1-mysql-error-log' : 'web1-mysql-error-log',
    'web1-apache2-error-log' : 'web1-apache2-error-log',
    'web2-mysql-error-log' : 'web2-mysql-error-log',
    'web2-apache2-error-log' : 'web2-apache2-error-log'
}






def get_fullpathes():
    


    print("\n\n\n")
    print("------------function starts------------")
    today = date.today()

    today_y = today.year
    today_m = today.month
    today_d = today.day

    print(today_d,today_m,today_y)
    print("sys.argv: ", sys.argv)


    if len(sys.argv) != 5:
        print("insufficient argvs")
        sys.exit()


    dateinput = "/" + sys.argv[1] + "/" + sys.argv[2] + "/" + sys.argv[3]
    print("dateinput: ", dateinput)


    print(os.getcwd())
    walkpath = "./" + dict_logtype[sys.argv[4]] + dateinput
    print("walkpath: ", walkpath)


    try :
        print(type(os.walk(walkpath)))
        print("good walkpath")

        a = next(os.walk(walkpath))
        print(type(a))
        print(a)

    except:
        print("no such walkpath")
        sys.exit()
    print(os.walk(walkpath))



    fullpathes = []
    for path, dires, files in os.walk(walkpath):
        print("-" * (len(path) + 10) )
        print("path: ", path)
        print("dires: ", dires)
        print("files: ", files)

        if len(files) > 0:
            print("existing files: ", files)
            for file in files :
                print("append: ", file)
                fullpathes.append(path + "/" + file)

        print("-" * (len(path) + 10) )

    print("path fin: ", path)


    print("fullpathes: ")
    for fullpath in fullpathes[1:]:
        print(fullpath)

    return fullpathes


# ----web1-mysql-error-log 합치기----------------------------------------------------
def S3_log_combine (fullpathes, logtype):
    print("\n\n\n")
    print("start COMBINE LOG: " + logtype + "\n\n")
    print(fullpathes)



    f_outpath = './' + 'tmp_' + logtype + '_combine' + '.txt'
    # print("f_outpath: ", f_outpath)
    # with open(f_outpath, 'w') as f_out:
    #     print("init f_out")
    #     f_out.write("init write")
    #     f_out.close()


    for fullpath in fullpathes[1:]:
        print(fullpath)

        with gzip.open(fullpath, 'rb') as frb:
            print("gzip.open(fullpath)")
            # print(frb.readlines())
            print("\n")


            with open(f_outpath, 'w+') as f_out:


                byte_lines = frb.readlines()
                for byte_line in byte_lines:
                    byte_inputline = byte_line
                    print(byte_inputline)
                    str_inputline = byte_inputline.decode("utf-8")
                    print(str_inputline)


                    f_out.write(str_inputline)


                f_out.close()
            frb.close()




# ----apache2-error 추출----------------------------------------------------
def dberror_analysis (fullpathes, logtype):
    print("\n\n\n")
    print("start" + logtype + "\n\n")
    print(fullpathes)



    f_outpath = './' + 'test_' + logtype + '_analysis' + '.txt'
    print("f_outpath: ", f_outpath)
    with open(f_outpath, 'w') as f_out:
        print("init f_out")
        f_out.write("init write")
        f_out.close()


    for fullpath in fullpathes[1:]:
        print(fullpath)

        with gzip.open(fullpath, 'rb') as frb:
            print("gzip.open(fullpath)")
            # print(frb.readlines())
            print("\n")


            with open(f_outpath, 'w+') as f_out:


                byte_lines = frb.readlines()
                for byte_line in byte_lines:
                    byte_inputline = byte_line
                    print(byte_inputline)
                    str_inputline = byte_inputline.decode("utf-8")
                    print(str_inputline)

                    split_inputline = str_inputline.split()
                    print(split_inputline)


                    #----logtime 필터링 및 작성----------------------------
                    logtime = []
                    try:
                        logtime.append(split_inputline[0])
                        logtime.append(split_inputline[0].split("T")[0])
                        logtime.append(split_inputline[0].split("T")[1].split(".")[0])
                        logtime.append(split_inputline[0].split("T")[1].split("Z")[0])


                        # logtime.append(split_inputline[1])
                        # logtime.append(split_inputline[2])
                        print("logtime: ", logtime)
                        for data in logtime:
                            f_out.write(data + " ")
                    #----logtime 필터링 및 작성 끝----------------------------



                        f_out.write(" \n")
                        print("----" * 25)
                    except:
                        print("possibly end of log")
                        print(split_inputline)




            f_out.close()
            frb.close()




# ----ct-log 추출----------------------------------------------------
def ctlog_analysis (fullpathes, logtype):
    print("\n\n\n")
    print("start" + logtype + "\n\n")
    print(fullpathes)



    f_outpath = './' + 'test_' + logtype + '_analysis' + '.txt'
    print("f_outpath: ", f_outpath)
    with open(f_outpath, 'w') as f_out:
        print("init f_out")
        f_out.write("init write")
        f_out.close()


    for fullpath in fullpathes[1:]:
        print(fullpath)

        with gzip.open(fullpath, 'rb') as frb:
            print("gzip.open(fullpath)")
            # print(frb.readlines())
            print("\n")


            with open(f_outpath, 'w+') as f_out:


                byte_lines = frb.readlines()
                for byte_line in byte_lines:
                    byte_inputline = byte_line
                    print(byte_inputline)
                    str_inputline = byte_inputline.decode("utf-8")
                    print(str_inputline)

                    split_inputline = str_inputline.split()
                    print(split_inputline)


                    #----logtime 필터링 및 작성----------------------------
                    logtime = []
                    try:
                        logtime.append(split_inputline[0])
                        logtime.append(split_inputline[0].split("T")[0])
                        logtime.append(split_inputline[0].split("T")[1].split(".")[0])
                        logtime.append(split_inputline[0].split("T")[1].split("Z")[0])


                        # logtime.append(split_inputline[1])
                        # logtime.append(split_inputline[2])
                        print("logtime: ", logtime)
                        for data in logtime:
                            f_out.write(data + " ")
                    #----logtime 필터링 및 작성 끝----------------------------



                        f_out.write(" \n")
                        print("----" * 25)
                    except:
                        print("possibly end of log")
                        print(split_inputline)




            f_out.close()
            frb.close()







# ----main------------------------------------------------------------
try:
    print("input logtype : ", dict_logtype[sys.argv[4]])
    logtype = dict_logtype[sys.argv[4]]


    fullpathes = get_fullpathes()
    print("\n\n\n")
    print("logtype: ", logtype)



    # S3_log_combine
    print("\n\n\n")
    print("logtype: ", logtype)
    S3_log_combine(fullpathes, logtype)
    print("logtype: ", logtype)
    print("S3_log_combine(", logtype,") done")


except:
    print("wrong logtype")
    print("dict_logtype: ", dict_logtype)
    sys.exit()








# # web1 error logs for mysql & apache2
# if "web1-mysql-error-log" == dict_logtype[sys.argv[4]]:
#     # mysql_errlog_combine
#     print("\n\n\n")
#     print("logtype: ", dict_logtype[sys.argv[4]])
#     mysql_errlog_combine1(fullpathes, dict_logtype[sys.argv[4]])
#     print("logtype: ", logtype)
#     print("mysql_errlog_combine1() done")

# elif "web1-apache1-error-log" == dict_logtype[sys.argv[4]]:
#     # ctlog_analysis
#     print("\n\n\n")
#     print("logtype: ", dict_logtype[sys.argv[4]])
#     ctlog_analysis(fullpathes, dict_logtype[sys.argv[4]])
#     print("logtype: ", logtype)
#     print("apache2_errlog_combine1() done")

# # web2 error logs for mysql & apache2
# if "web2-mysql-error-log" == dict_logtype[sys.argv[4]]:
#     # mysql_errlog_combine
#     print("\n\n\n")
#     print("logtype: ", dict_logtype[sys.argv[4]])
#     mysql_errlog_combine2(fullpathes, dict_logtype[sys.argv[4]])
#     print("logtype: ", logtype)
#     print("mysql_errlog_combine2() done")

# elif "web2-apache2-error-log" == dict_logtype[sys.argv[4]]:
#     # ctlog_analysis
#     print("\n\n\n")
#     print("logtype: ", dict_logtype[sys.argv[4]])
#     ctlog_analysis(fullpathes, dict_logtype[sys.argv[4]])
#     print("logtype: ", logtype)
#     print("apache2_errlog_combine2() done")



    # 'web1-mysql-error-log' : 'web1-mysql-error-log',
    # 'web1-apache2-error-log' : 'web1-apache2-error-log',
    # 'web2-mysql-error-log' : 'web2-mysql-error-log',
    # 'web2-apache2-error-log' : 'web2-apache2-error-log'








dict_logtype = {
    "ct-log" : "ct-log",
    "mysql-error" : "mysql-error.log",
    "s3lambda" : "aws-lambda-beom-cw-s3",
    "messagelog" : "messagelog",
    "db-error" : "aws-rds-instance-dev-db-error"
}

# # path = path.replace("\\", "/")
# print("path fin: ", path)
# fullpathes = []
# for file in files :
#     fullpathes.append(path + "/" + file)
#
# count = 0
# for fullpath in fullpathes :
#     print("fullpath", count, ": ", fullpath)
# #     count += 1
#
#
#
# path = fullpathes[0]


# with gzip.open(path, 'rb') as frb:
#     print("gzip.open(path) \n\n\n")
#     # print(frb.readlines())
#     print("\n\n\n")
#
#     byte_inputline = frb.readline()
#     print(byte_inputline)
#     findindex = byte_inputline.find(b"Z {")
#     print("findindex: ", findindex)
#
#
#     print("byte_time: ", byte_inputline[:findindex + 1])
#     byte_time = byte_inputline[:findindex + 1]
#     str_time = byte_time.decode("utf-8")
#     print("str_time: ", str_time)
#
#     print(byte_inputline[findindex + 1:])
#     byte_inputline = byte_inputline[findindex + 1:]
#
#
#
#     str_inputline = byte_inputline.decode("utf-8")
#     print("str_inputline: ", str_inputline)
#
#
#     json_input = json.loads(str_inputline)
#     print(json_input)
#
#
#
#     # with open('./' + 'test.txt', 'wb') as f_out:
#     #     f_out.writelines(frb)
#     #
#     #
#     #
#     # f_out.close()
#     frb.close()
