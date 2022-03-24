# Authors: 	Tzortzis Alexandros-Menelaos, 2638
#			Pavlidis Panagiotis, 2608
# Team: AB
# Execution: 	Providing you have installed a python environment into your system,
# 				simply run client.py, no arguments required, all variables have been found
#				beforehand and hardcoded into the script 
# 				Run in cmd/terminal in the directory the file is in: "python ./client.py" 


# This code is part of the winter semester's exercise for the course "Network Protocol Design"
# More specifically, it represents the client that remains a client at the duration of the
# execution and communicates with three different servers
	
import socket
import copy

TCP_HOST = '10.8.0.1'  			# The TCP server's hostname or IP address
TCP_PORT = 65432       			# The port used by the server

my_IP = b'10.8.0.26' 			# client's IP address
my_MAC = b'00:ff:8b:20:bf:ca'	# client's MAC address 
my_AEM = b'2638'				# client's AEM
my_TEAM = b'AB'					# client's team

client_HOST = '10.8.0.25'		# teammate's IP address
client_PORT = 65433				# teammate's port number

UDP_HOST = '10.8.0.1'			# The UDP server's hostname or IP address
UDP_PORT = 65433				# The port used by the UDP server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:	#create a TCP socket
    s.connect((TCP_HOST,TCP_PORT)) 	# establish connection with given TCP server
    s.sendall(my_IP)				# send my IP address for evaluation
    data = s.recv(1024)				# recieve reply from evaluation
    print('Received from TCP: ', repr(data))	# print reply
    s.sendall(my_MAC)				# send my MAC address (according to the VPN Network) for evaluation
    data = s.recv(1024)				# recieve reply from evaluation
    print('Received from TCP: ', repr(data))	# print reply
    s.sendall(my_AEM)				# send my personal AEM for evaluation
    data = s.recv(1024)				# recieve reply from evaluation
    print('Received from TCP: ', repr(data))	# print reply
    s.sendall(my_TEAM)				# send my team's name for evaluation
    data = s.recv(1024)				# recieve reply from evaluation (personal token if valid)
    print('Received from TCP: ', repr(data))	#print reply

token = copy.deepcopy(data) #create a deep copy of the token in case it is needed
print('Token recieved from TCP: ', token)		#print token

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:	#create a TCP socket
    s.connect((client_HOST, client_PORT))		# establish connection with my teammate's TCP server
    s.sendall(token)							# send your personal token
    combinedToken = s.recv(1024)				# recieve from teammate the combined token of his and mine

print('Received combinedToken from teammate\'s server: ', repr(combinedToken)) # print combined token

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s: # create a UDP socket
    s.sendto(combinedToken,(UDP_HOST,UDP_PORT))				# send combined token to the server given UDP server
    data,addr = s.recvfrom(2048)							# recieve reply (success/fail if it was valid)
    expectedToken = s.recvfrom(2048)						# recieve expected token (used in case of failure)

#print the result
print('Received from UDP with address: {} the message: {}'.format(addr,data))
print("Expected token should be: ",expectedToken[0])
print("for UDP server: ",expectedToken[1])
