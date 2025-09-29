import os
import re
import ipwhois

open("asnoutput.txt", "w").close()

ipList = open("iplist.txt", "r")
for destination in ipList:
    destination = destination.strip()
    with open("asnoutput.txt", "a") as file:
        file.write("\n--------------------\n")
        file.write("Traceroute for " + destination + "\n")

    myData = os.popen('tracert -4 ' + destination).read()
    route = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', myData)[1:]

    for ip in route:
        print(ip)
        try:
            myIp = ipwhois.net.Net(ip)
            results = myIp.lookup_asn()
            outputData = [ip, results['asn'], results['asn_description']]
        except:
            outputData = [ip, "Non-lookupable IP address."]
        with open("asnoutput.txt", "a") as file:
            file.write(str(outputData) + "\n")
