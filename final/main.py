# -*- coding: utf-8 -*-
import sys
import json
import csv
import socket
import pickle
import collections
from dbscan import *
# 192.168.0.4
HOST = ''
PORT = 8080


def checkFileExist(filePath):
    try:
        with open(filePath, 'r') as f:
            return True
    except FileNotFoundError as e:
        return False
    except IOError as e:
        return False


# 1. open socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print('socket created')
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 2. bind to a address and port

try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Bind Failed. error code' + str(msg[0]) + 'Message' + msg[1])
    sys.exit()

print('Socket bind complete')

# 3. Listen for incoming connections
s.listen(10)
print('Socket now listening')
conn, addr = s.accept()
# keep talking with the client
count = 0
temp_list = []
hum_list = []
gas_list = []
label_list = []
label = []
while 1:
    # 4. Accept connection

    # 5. Read/Send

    print('Connected with ' + addr[0] + ':' + str(addr[1]))
    data = conn.recv(65535)
    # json_data = data.decode()
    # filename=str(json_data["Time"])
    # with open(filename+'.csv', 'wt', encoding='utf-8') as f
    print('receive data:', data.decode())
    if data == None:
        break
    datum = json.loads(data.decode())
    # ���⼭�� ������ �ִ��� ������ ��� row���� Ȯ���ϴ� �Ŵϱ� ������ ������ ���� ���� ���ϴ°� �����ҵ�
    name = str(datum['Time']).split(" ")[0]
    output_file_name = ("%s.csv" % name)
    # ��¥�� �ٲ� ����� data�� csv���Ϸ� �������
    temp_list.append(datum['temparature'])
    hum_list.append(datum['humidity'])
    gas_list.append(datum['LPG'])
    label_list.append(datum['label'])
    if checkFileExist("%s.csv" % name) == False:
      with open(output_file_name, 'w', encoding='utf-8') as output_file:
            csvwriter = csv.writer(output_file)
            csvwriter.writerow(["TIME", "TEMP", "HUM", "LPG", "LABEL"])
            csvwriter.writerow([datum['Time'], datum['temparature'], datum['humidity'], datum['LPG'], datum['label']])

    if checkFileExist("%s.csv" % name) == True:
        with open(output_file_name, 'a', encoding='utf-8') as output_file:
            csvwriter = csv.writer(output_file)
            csvwriter.writerow([datum['Time'], datum['temparature'], datum['humidity'], datum['LPG'], datum['label']])

        output_file.close()

    if count >= 50 and count % 10==0:
        label = dbscan(temp_list[count-50:count], hum_list[count-50:count], gas_list[count-50:count], label_list[count-50:count])
        label = map(str, label)
        data_s = " ".join(label)
        conn.sendall(data_s.encode())
    else:
        reply = "send"
        
        conn.sendall(reply.encode())

    count += 1

conn.close()
s.close()
print('close')