import subprocess, re, ipwhois

def trace(ip):
    try:
        result = subprocess.run(
            ["tracert", ip],
            capture_output=True,
            text=True,
            shell=True
        )
        output = result.stdout
        # Debug: show first lines if needed
        # print("Traceroute raw output:\n", output)
        # Match IPv4 addresses, with or without brackets
        route = re.findall(r"\[?(\d{1,3}(?:\.\d{1,3}){3})\]?", output)
        return route
    except Exception as e:
        print(f"Traceroute failed for {ip}: {e}")
        return []

def asn(ip):
    try:
        myIp = ipwhois.Net(ip)
        myObj = ipwhois.asn.IPASN(myIp)
        return myObj.lookup()
    except Exception as e:
        print(f"ASN lookup failed for {ip}: {e}")
        return None

# test
if __name__ == "__main__":
    ips = trace("8.8.8.8")
    print("Route:", ips)
    for ip in ips:
        print(ip, asn(ip))
