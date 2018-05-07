import requests
import json
import time

global gyldigServerData
gyldigServerData = 1

#grunnoppsett for kommunikasjon med serveren
def serverCom(bronnid, get, sdata):

    url1 = "http://158.38.120.54:8000/csrf"
    url2 = "http://158.38.120.54:8000/data"
    client = requests.session()
    client.get(url1)
    csrftoken = client.cookies['csrftoken']

    l_data = dict(csrfmiddlewaretoken=csrftoken,
                  bronnid=bronnid,
                  timestamp=time.time(),
                  get = get, next='/')
    
    if len(sdata) != 0:
        for x in sdata:
            l_data[x] = sdata[x]

    r = client.post(url2, data=l_data, headers=dict(Referer=url2))
    return(json.loads(r.content.decode()))

def serverSend(bronnid, sdata):     #forenklet funksjon for å sende data
    global gyldigServerData
    gyldigServerData = 0
    mdata = serverCom(bronnid,0,sdata)
    return mdata

def serverHent(bronnid):        #forenklet funksjon for å hente data
    global gyldigServerData
    gyldigServerData = 1
    mdata = serverCom(bronnid,1,{})
    if gyldigServerData == 1:
        return mdata
    else:
        return None
