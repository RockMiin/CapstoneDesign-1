import sys
import socket
# 192.168.0.4
HOST = ''
PORT = 8080

# 1. open socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print('socket created')
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 2. bind to a address and port

try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Bind Failed. error code' + str(msg[0]) + 'Message' + msg[1] )
    sys.exit()

print('Socket bind complete')

# 3. Listen for incoming connections
s.listen(10)
print('Socket now listening')
conn, addr = s.accept()
# keep talking with the client
while 1:
    # 4. Accept connection


    # 5. Read/Send
    
    print('Connected with ' + addr[0] + ':' + str(addr[1]))
    data = conn.recv(65535)
    print('receive data:', data.decode())
    if data == None:
        break

conn.close()
s.close()
print('close')
