#	Command Lines: run with dns-client.py 127.0.0.1 9999 host1.student.test
import sys
import socket
import struct
import time
import random
# Get the server hostname, port and data length as command line arguments
host = sys.argv[1]
port = int(sys.argv[2])

# Create UDP client socket. Note the use of SOCK_DGRAM
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientsocket.settimeout(1)
colors = ["red", "orange", "yellow", "green", "blue", "purple", "unspecified color", "do not change"]

def isON(on):
	if on:
		return "ON"
	return "OFF"

try:
	commandType = int(sys.argv[3])
except:
	commandType = -1

try:
	if commandType == 0 or commandType == 1:
		color = sys.argv[4] #color required
	else:
		color = 6 #unspecified
except:
	color = 6
on = 1
messageID = random.randint(1, 100)
errorCode = 0
messageType = 1

#convert "red" to 0
for i in range(0, len(colors)):
	if color == colors[i]:
		color = i
		break
if type(color) == str:
	color = 8


print(f"Sending Request to {host}, {port}:")
# print(f"on?: {on}")
print(f"Command Type: {commandType}")
print(f"Message ID:   {messageID}")
print(f"Color Requested: {color}")
# print(f"errorCode: {errorCode}")
# print(f"messageType: {messageType}")
print()
#				messageType, returnCode
data = struct.pack(f"!hhihhi", on, color, messageID, commandType, errorCode, messageType)
for i in range(3): # try 3 times
	clientsocket.sendto(data,(host, port))
	try:
		response, address = clientsocket.recvfrom(1024)
		on, color, messageID, commandType, errorCode, messageType = struct.unpack_from(f"!hhihhi", response)
		print(f"Received response from {host}, {port}:")
		print(f"Error Code: {errorCode}")
		print(f"Message ID: {messageID}")
		print(f"Color: {color}")
		print(f"Lightbulb: {isON(on)}")
		break
	except socket.error:
		if i < 2:
			print("Request timed out ...")
			print(f"Sending Request to {host}, {port}:")
		else:
			print("Request timed out ... Exiting Program.")
#Close the client socket
clientsocket.close()