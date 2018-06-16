# -*- coding utf-8 -*-
import urllib
import urllib.request
import urllib.error
import json
def getproperty(sta):
    L=[]
    url1 = "http://shuyantech.com/api/cndbpedia/ment2ent?q="+urllib.parse.quote(sta)  
    req1 = urllib.request.Request(url1)

    try:
        urllib.request.urlopen(req1)
    except urllib.error.URLError as e:
        L.append(e.reason)
        print(L)
        return L

    
    response1 = urllib.request.urlopen(req1)
    result1 = response1.read().decode()
    result1 = json.loads(result1)    
    if(result1['status'] != 'ok'):
        L.append('FAILED')
        print(L)
        return L

    elif(  len( result1['ret'] )  != 0 ):
        stb = result1['ret'][0]
    else:
        L.append('NO LABEL')
        print(L)
        return L

    url2 = "http://shuyantech.com/api/cndbpedia/avpair?q="+urllib.parse.quote(stb)  
    req2 = urllib.request.Request(url2)
    response2 = urllib.request.urlopen(req2)
    result2 = response2.read().decode()
    result2 = json.loads(result2)    
    if(result2['status'] != 'ok'):
        L.append('FAILED')
        print(L)
        return L
    else:
        L.append('OK')
        i=1
        for string in result2['ret'] :
            if( i > 3  or string[0]=='DESC' ):
                break
            L.append(string[1])
            i=i+1
        print(L)
        return L
    #        return(result['ret'])
