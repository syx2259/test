#!/usr/bin/env python

# This client demonstrates Thrift's connection and "oneway" asynchronous jobs
# Client connects to server host:port and calls 2 methods
# showCurrentTimestamp : which returns current time stamp from server
# asynchronousJob() : which calls a "oneway" method
#

# host = "localhost"
# port = 9090

from asyncio import futures
import sys
import time
from concurrent.futures import ThreadPoolExecutor

# your gen-py dir
sys.path.append('../gen-py')

# Example files
from Example import *
from Example.ttypes import *

# Thrift files
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


def requestOne(host, port, index):
    transport = TSocket.TSocket(host, port)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = Example.Client(protocol)
    transport.open()
    if index == 0:
        #f = open("rtt.txt", "w")
        #f = open("rtt_one_cpu_intensive.txt", "w")
        #f = open("rtt_two_cpu_intensive.txt", "w")
        #f = open("rtt_three_cpu_intensive.txt", "w")
        f = open("rtt_four_cpu_intensive.txt", "w")
        for x in range(100000):
            startTime = time.time()
            # Run showCurrentTimestamp() method on server
            currentTime = client.showCurrentTimestamp()
            endTime = time.time()
            interval = endTime - startTime
            f.write(str(interval) + "\n")
        f.close()
    else :
        # Run showCurrentTimestamp() method on server
        currentTime = client.showCurrentTimestamp()
    transport.close()
    return "Finish work in " + host

def requestAll(hosts):
    futures_list = []
    results = []
    with ThreadPoolExecutor(max_workers=6) as executor:
        index = 0
        for host in hosts:
            futures = executor.submit(requestOne, host, 9090, index)
            futures_list.append(futures)
            index += 1

        for future in futures_list:
            try:
                result = future.result(timeout=30)
                results.append(result)
            except Exception:
                results.append(None)
    return results

if __name__ == "__main__":
    try:
        #hosts = ("10.0.2.21", "10.0.2.22", "10.0.2.23", "10.0.2.24", "10.0.2.25")
        #hosts = ("10.0.2.21", "10.0.2.22")
        #results = requestAll(hosts)
        #for result in results:
        #    print(result)
        requestOne("10.0.2.21", 9090, 0)
        # Init thrift connection and protocol handlers
        # transport = TSocket.TSocket( host , port)
        # transport = TTransport.TBufferedTransport(transport)
        # protocol = TBinaryProtocol.TBinaryProtocol(transport)

        # # Set client to our Example
        # client = Example.Client(protocol)

        # # Connect to server
        # transport.open()

        # # startTime of RTT
        # startTime = time.time()

        # # Run showCurrentTimestamp() method on server
        # currentTime = client.showCurrentTimestamp()

        # # Calculate the RTT
        # endTime = time.time()
        # print("RTT: " + str(endTime - startTime))
        # print("Request result: " + currentTime)

        # Assume that you have a job which takes some time
        # but client sholdn't have to wait for job to finish
        # ie. Creating 10 thumbnails and putting these files to sepeate folders
        #client.asynchronousJob()


        # Close connection
        # transport.close()
    except Thrift.TException as tx:
        print('Something went wrong : %s' % (tx.message))

