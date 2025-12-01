from socket import *
import socket
import os
import sys
import struct
import time
import select
import binascii

# Dont worry about this method


def checksum(string):
    csum = 0
    countTo = (len(string) / 2) * 2

    count = 0
    while count < countTo:
        thisVal = string[count+1] * 256 + string[count]
        csum = csum + thisVal
        csum = csum & 0xffffffff
        count = count + 2

    if countTo < len(string):
        csum = csum + string[len(string) - 1]
        csum = csum & 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


def receiveOnePing(mySocket, ID, timeout, destAddr):
    time_left = timeout
    while 1:
        time_start = time.time()
        # Wait for the socket to receive a reply
        buffer = select.select([mySocket], [], [], time_left)

        # If we do not get a response within the timeout
        if not buffer[0]:
            return "Request timed out."
        time_received = time.time()

        # Code Start
        # Receive the packet and address from the socket
        # Code End

        # Code Start
        # Extract the ICMP header from the IP packet
        # Code End

        # Code Start
        # Use struct.unpack to get the data that was sent via thestruct.pack method below
        # Code End

        # Code Start
        # Verify Type/Code is an ICMP echo reply
        # Code End

        # Code Start
        # Extract the time in which the packet was sent
        # Code End

        # Code Start
        # Return the delay in ms: 1000 * (time received - time sent)
        # Code End

        # If we got a response but it was not an ICMP echo reply
        time_left = (time_received - time_start)
        if time_left <= 0:
            return "Request timed out."


def sendOnePing(mySocket, destAddr, ID):
    # Header is type (8), code (8), checksum (16), id (16), sequence(16)
    myChecksum = 0
    # Make a dummy header with a 0 checksum
    # struct -- Interpret strings as packed binary data

    # Code Start

    # Define icmpEchoRequestType and
    # icmpEchoRequestCode, which are both used below
    # Code End

    header = struct.pack("bbHHh", icmpEchoRequestType,
                         icmpEchoRequestCode, myChecksum, ID, 1)

    data = struct.pack("d", time.time())
    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(header + data)

    # Get the right checksum, and put in the header
    if sys.platform == 'darwin':
        myChecksum = socket.htons(myChecksum) & 0xffff
    # Convert 16-bit integers from host to network byte order.
    else:
        myChecksum = socket.htons(myChecksum)

    header = struct.pack("bbHHh", icmpEchoRequestType,
                         icmpEchoRequestCode, myChecksum, ID, 1)
    packet = header + data

    # AF_INET address must be tuple, not str
    mySocket.sendto(packet, (destAddr, 1))


def doOnePing(destAddr, timeout):
    icmp = socket.getprotobyname("icmp")
    # SOCK_RAW is a powerful socket type.
    # For more details see: http://sock-raw.ord/papers/sock_raw
    # Code Start
    # Create Socket here
    # Fill in end

    myID = os.getpid() & 0xFFFF  # Return the current process i
    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)

    mySocket.close()
    return delay


def ping(host, timeout=1):
    # timeout=1 means: If one second goes by without a reply from the server,
    # the client assumes that either the
    # client's ping or the server's pong is lost
    dest = socket.gethostbyname(host)
    print("Pinging " + dest + " using Python:\n")
    # Send ping requests to a server separated by approximately one second
    while 1:
        delay = doOnePing(dest, timeout)
        print(delay)
        time.sleep(1)  # one second
    return delay


ping("google.com")
