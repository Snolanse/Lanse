import requests
import json
import time

global gyldigServerData
gyldigServerData = 1

def serverCom(bronnid, get, sdata):

    url1 = "http://192.168.0.101:8000/csrf"
    url2 = "http://192.168.0.101:8000/test"
    client = requests.session()
    client.get(url1)
    csrftoken = client.cookies['csrftoken']

    l_data = dict(csrfmiddlewaretoken=csrftoken, bronnid=bronnid, timestamp=time.time(), get = get, next='/')
    
    if len(sdata) != 0:
        for x in sdata:
            l_data[x] = sdata[x]



    r = client.post(url2, data=l_data, headers=dict(Referer=url2))
    return(json.loads(r.content.decode()))

def serverSend(bronnid, sdata):
    global gyldigServerData
    gyldigServerData = 0
    mdata = serverCom(bronnid,0,sdata)
    return mdata

def serverHent(bronnid):
    global gyldigServerData
    gyldigServerData = 1
    mdata = serverCom(bronnid,1,{})
    if gyldigServerData == 1:
        global serverData
        serverData = mdata
