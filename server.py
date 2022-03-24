# Panagiotis Pavlidis 2608
# Alexandros Tzortzis 2638

import socket

HOST = '10.8.0.1'   			# The server's hostname or IP address
PORT = 65432        			# The port used by the server

my_IP = b'10.8.0.25'			
my_MAC = b'00:ff:11:2b:a1:2d'	
my_AEM = b'2608'
my_TEAM = b'AB'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    s.sendall(my_IP)
    data = s.recv(1024)
    print('Received', repr(data))
    
    s.sendall(my_MAC)
    data = s.recv(1024)
    print('Received', repr(data))

    s.sendall(my_AEM)
    data = s.recv(1024)
    print('Received', repr(data))

    s.sendall(my_TEAM)
    data = s.recv(1024)

    token = data

    print('Received', repr(token))

    # 2nd part

    HOST = '10.8.0.25'		# Our server's ip address	
    PORT = 65433        	# The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                new_token = token + data    
                conn.sendall(new_token)

    print(new_token)

    # 3rd part

    HOST = '10.8.0.1'  	# The server's hostname or IP address
    PORT = 65433        # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:                

        s.sendto(new_token,(HOST,PORT))
        data, addr = s.recvfrom(1024)
        print('Received', repr(data))
        print(addr)

        data, addr = s.recvfrom(1024)
        print('Received', repr(data))
        print(addr)
