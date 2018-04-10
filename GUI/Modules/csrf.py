import requests
import json

def serverCom(bronnid, get, sdata):

    url1 = "http://192.168.0.101:8000"
    url2 = "http://192.168.0.101:8000/test"
    client = requests.session()
    client.get(url1)
    csrftoken = client.cookies['csrftoken']

    l_data = dict(csrfmiddlewaretoken=csrftoken, bronnid=bronnid, get = get, next='/')
    
    if len(sdata) != 0:
        for x in sdata:
            l_data[x] = sdata[x]

    r = client.post(url2, data=l_data, headers=dict(Referer=url2))
    return(json.loads(r.content.decode()))