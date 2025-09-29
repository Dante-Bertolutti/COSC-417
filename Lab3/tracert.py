import os, re, ipwhois

def trace(ip) :
    myData = os.popen('tracert ' + ip).read()
    route = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', myData[1:])
    return route

def asn(ip) :
    try:
        myIp = ipwhois.Net(ip)
        myObj = ipwhois.asn.IPASN(myIp)
        results = myObj.lookup()
        return results
    except:
        return None

ips = trace('8.8.8.8')
for ip in ips :
    print(asn(ip))