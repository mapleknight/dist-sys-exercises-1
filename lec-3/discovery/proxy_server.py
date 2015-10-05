#!/usr/bin/env python

#******************************************************************************
#
#  CS 6421 - Simple Conversation
#  Execution:    python prox_server.py portnum
#
#******************************************************************************

import socket
import sys


class ConversionServer:
    def __init__(self, addr, portnum, conv_in, conv_out):
        self.addr=addr
        self.portnum=portnum
        self.conv_in=conv_in
        self.conv_out=conv_out

    def convert(self, input_amount):
        # Create a socket 
        tmpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to server 
        print("Connecting to : " + self.addr + " " + self.portnum)
        tmpsock.connect((self.addr, int(self.portnum)))

        tmpsock.send(self.conv_in + " " + self.conv_out + " " + input_amount + "\n")
        result = tmpsock.recv(BUFFER_SIZE)
        tmpsock.close()
        # Return the conversion result 
        return result  

    def __str__(self):
        return self.addr+":"+self.portnum+":"+self.conv_in+":"+self.conv_out

    def __repr__(self):
        return self.addr+":"+self.portnum+":"+self.conv_in+":"+self.conv_out

## Function to process requests
def process(conn):
    conn.send("Welcome, you are connected to a proxy server\n")

    # read userInput from client
    userInput = conn.recv(BUFFER_SIZE)
    if not userInput:
        print "Error reading message"
        sys.exit(1)

    print "Received message: ", userInput
    # TODO: add convertion function here, reply = func(userInput)
    reply = func(userInput)
    conn.send(str(reply) + "\n")   
    
    conn.close()
    
def func(userInput):
    inputtokens = userInput.split(" ")
    input_unit = inputtokens[0]
    output_unit = inputtokens[1]
    input_amount = inputtokens[2]

    try:
        return servers[input_unit+output_unit].convert(input_amount) 
    except KeyError:
        if input_unit == "in" and output_unit == "m" or input_unit == "m" and output_unit == "in":
            firstConv = servers[input_unit+"cm"].convert(input_amount) 
            secondConv = servers["cm"+output_unit].convert(firstConv)
            return secondConv
        else:
            return "Your input units are not supported!"
    
### Main code run when program is started
BUFFER_SIZE = 1024
interface = ""

# if input arguments are wrong, print out usage
# TODO add error checking

myPubIP = int(sys.argv[1])
portnum = int(sys.argv[2])
DisServerIP = int(sys.argv[3])
DisServer_portNum = int(sys.argv[4])
servers = {}

#register servers in the format addr:portnum:inunit:outunit
for i in range(5,len(sys.argv)):
    serverinfo=sys.argv[i].split(":")
    servers[serverinfo[2]+serverinfo[3]]=ConversionServer(serverinfo[0],serverinfo[1],serverinfo[2],serverinfo[3])
    servers[serverinfo[3]+serverinfo[2]]=ConversionServer(serverinfo[0],serverinfo[1],serverinfo[3],serverinfo[2])

#print(servers)

# fucntion to add/remove entries from Discovery Server
def add_remove(req):
    if req.lower() == "add" or req.lower() == "remove":
        try:
            # create a socket and connect to the Discovery Server
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((DisServerIP, DisServer_portNum))
            print "Sending '" + req + " in m " + myPubIP + " " + portnum + "' " + "to the Discovery Server"
            sock.send(req + " in m " + myPubIP + " " + portnum)
            userInput = sock.recv(BUFFER_SIZE)
            print "Response from Discovery Server: " + userInput
            sock.close()
        except:
        print "Connection error"
    else:
        print "Your input must be 'ADD' or 'REMOVE' (case-insensitive)"

try:
# create socket to receive connection 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((interface, portnum))
    s.listen(5)
except:
    print "Connection error"

print "Enter ADD/REMOVE (case-insensitive) anytime to add/remove proxy server to/from the Discovery Server"
while True:
    add_remove(input())
    # accept connection and print out info of client
    conn, addr = s.accept()
    print 'Accepted connection from client', addr
    process(conn)
s.close()
