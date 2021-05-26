#	Command Lines: run with server.py 127.0.0.1 9999
import sys
import socket
import struct
import random
import time
# Read server IP address and port from command-line arguments
serverIP = sys.argv[1]
serverPort = int(sys.argv[2])

def isON(on):
	if on:
		return "ON"
	return "OFF"

def setColor():
	global color, errorCode, CURRENTCOLOR, CURRENTCOLORCODE
	#set color
	if color < 6:
		CURRENTCOLOR = colors[color]
		CURRENTCOLORCODE = color
	elif color == 6: #unspecified (random)
		CURRENTCOLORCODE = random.randint(0, len(colors)-1)
		CURRENTCOLOR = colors[CURRENTCOLORCODE]
	elif color == 7: #don't change
		color = CURRENTCOLORCODE
	else:
		color = CURRENTCOLORCODE
		errorCode = 2 #not supported
	CURRENTCOLORCODE = color

def setON():
	global on, CURRENTON
	CURRENTON = 1
	on = 1
def setOFF():
	global on, CURRENTON
	CURRENTON = 0
	on = 0

#						0					1						2						3
# commands: |turn on and set color| |change color| |return status (on/off) and color| |turn off|

# 			0		1			2		3		4		5				6					7
colors = ["red", "orange", "yellow", "green", "blue", "purple", "unspecified color", "do not change"]
CURRENTCOLOR = "red"
CURRENTCOLORCODE = 0 
CURRENTON = 0 #off
# Create a UDP socket. Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Assign server IP address and port number to socket
serverSocket.bind((serverIP, serverPort))

print("The server is ready to receive on port:  " + str(serverPort) + "\n")

# loop forever listening for incoming UDP messages
while True:
	# Receive and print the client data from "data" socket
	request, address = serverSocket.recvfrom(1024)
	on, color, messageID, commandType, errorCode, messageType = struct.unpack(f"!hhihhi", request)
	# time.sleep(random.random()*.7) #give a random latency
# ========================================================================
	if messageType != 1 or color < 0 or errorCode != 0:
		errorCode = 1
	elif messageType == 1 and color > 5:
		errorCode = 1
	else:
		errorCode = 0

	#set mesasge to 2
	messageType = 2
	messageID = random.randint(1, 100)

	#commands
	if commandType == 0: #turn on and set color 
		setON()
		setColor()
	if commandType == 1: #change color
		setColor()
	if commandType == 2: #return status ('on') and color
		on = CURRENTON
		color = CURRENTCOLORCODE
	if commandType == 3: #turn off 
		setOFF()


	print(f"Sending response to {serverIP} {serverPort}")
	print(f"Message ID: {messageID}")
	if errorCode != 0:
		print(f"Color: {color}")
		print(f"Lightbulb: {isON(on)}")
	response = struct.pack(f"!hhihhi", on, color, messageID, commandType, errorCode, messageType)
	serverSocket.sendto(response, address)