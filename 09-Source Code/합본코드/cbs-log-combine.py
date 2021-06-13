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


# 파이썬 3버전 (3.X 버전)




# 입력받을 수 있는 로그타입에 대한 json 형식 변수
dict_logtype = {
    'web1-mysql-error-log' : 'web1-mysql-error-log',        # <=입력받는 로그 종류 : 해당 로그 폴더 상대경로
    'web1-apache2-error-log' : 'web1-apache2-error-log',
    'web2-mysql-error-log' : 'web2-mysql-error-log',
    'web2-apache2-error-log' : 'web2-apache2-error-log'
}





# 입력받은 로그파일들에 대한 경로들을 구한다.
def get_fullpathes():
    


    print("\n\n\n")
    print("------------function starts------------")
    today = date.today()        

    today_y = today.year
    today_m = today.month
    today_d = today.day

    print(today_d,today_m,today_y)
    print("sys.argv: ", sys.argv)


    # 파이썬 실행시 충분한 갯수의 인자값들이 있는지 확인
    if len(sys.argv) != 5:
        print("insufficient argvs")
        sys.exit()


    # sys.argv[1]=년, sys.argv[2]=월, sys.argv[3]=일
    dateinput = "/" + sys.argv[1] + "/" + sys.argv[2] + "/" + sys.argv[3]
    print("dateinput: ", dateinput)


    # sys.argv[4]=입력받은 로그타입
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




# ----입력받은 logtype의 복수의 로그 파일들을 합치기----------------------------------------------------
def S3_log_combine (fullpathes, logtype):
    print("\n\n\n")
    print("start COMBINE LOG: " + logtype + "\n\n")
    print(fullpathes)



    f_outpath = './' + 'tmp_' + logtype + '_combine' + '.txt'
    # print("f_outpath: ", f_outpath)



    
    for fullpath in fullpathes[1:]:     # aws-logs-write-test 파일에 대한 경로를 제외하기 위해 fullpathes의 범위를 [1:]로 한다.
        print(fullpath)

        with gzip.open(fullpath, 'rb') as frb:      # 해당 gzip 형태의 로그파일을 읽는다.
            print("gzip.open(fullpath)")
            # print(frb.readlines())
            print("\n")


            with open(f_outpath, 'w+') as f_out:

                
                # byte로 읽은 데이터를 utf-8로 디코딩 후 기록한다.
                byte_lines = frb.readlines()
                for byte_line in byte_lines:
                    byte_inputline = byte_line
                    print(byte_inputline)
                    str_inputline = byte_inputline.decode("utf-8")
                    print(str_inputline)


                    f_out.write(str_inputline)


                f_out.close()
            frb.close()




# # ----apache2-error 추출----------------------------------------------------
# def dberror_analysis (fullpathes, logtype):
#     print("\n\n\n")
#     print("start" + logtype + "\n\n")
#     print(fullpathes)



#     f_outpath = './' + 'test_' + logtype + '_analysis' + '.txt'
#     print("f_outpath: ", f_outpath)
#     with open(f_outpath, 'w') as f_out:
#         print("init f_out")
#         f_out.write("init write")
#         f_out.close()


#     for fullpath in fullpathes[1:]:
#         print(fullpath)

#         with gzip.open(fullpath, 'rb') as frb:
#             print("gzip.open(fullpath)")
#             # print(frb.readlines())
#             print("\n")


#             with open(f_outpath, 'w+') as f_out:


#                 byte_lines = frb.readlines()
#                 for byte_line in byte_lines:
#                     byte_inputline = byte_line
#                     print(byte_inputline)
#                     str_inputline = byte_inputline.decode("utf-8")
#                     print(str_inputline)

#                     split_inputline = str_inputline.split()
#                     print(split_inputline)


#                     #----logtime 필터링 및 작성----------------------------
#                     logtime = []
#                     try:
#                         logtime.append(split_inputline[0])
#                         logtime.append(split_inputline[0].split("T")[0])
#                         logtime.append(split_inputline[0].split("T")[1].split(".")[0])
#                         logtime.append(split_inputline[0].split("T")[1].split("Z")[0])


#                         # logtime.append(split_inputline[1])
#                         # logtime.append(split_inputline[2])
#                         print("logtime: ", logtime)
#                         for data in logtime:
#                             f_out.write(data + " ")
#                     #----logtime 필터링 및 작성 끝----------------------------



#                         f_out.write(" \n")
#                         print("----" * 25)
#                     except:
#                         print("possibly end of log")
#                         print(split_inputline)




#             f_out.close()
#             frb.close()





# ----main------------------------------------------------------------
try:
    print("input logtype : ", dict_logtype[sys.argv[4]])
    logtype = dict_logtype[sys.argv[4]]


    # 입력받은 로그타입의 로그파일 경로 탐색 함수 실행
    # 타입: 
    # 'web1-mysql-error-log' 
    # 'web1-apache2-error-log' 
    # 'web2-mysql-error-log' 
    # 'web2-apache2-error-log'
    fullpathes = get_fullpathes()
    print("\n\n\n")
    print("logtype: ", logtype)



    # S3_log_combine
    # 복수의 로그파일을 하나로 합치는 함수를 실행
    print("\n\n\n")
    print("logtype: ", logtype)
    S3_log_combine(fullpathes, logtype)
    print("logtype: ", logtype)
    print("S3_log_combine(", logtype,") done")


except:
    print("wrong logtype")
    print("dict_logtype: ", dict_logtype)
    sys.exit()


