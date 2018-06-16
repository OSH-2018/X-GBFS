# -*- coding utf-8 -*-
import urllib
import urllib.request
import urllib.error
import json
def getproperty(sta):
    L=[]
    sta = str.lower(sta)
    url1 = "http://shuyantech.com/api/cndbpedia/ment2ent?q="+urllib.parse.quote(sta)  
    req1 = urllib.request.Request(url1)

    try:
        response1 = urllib.request.urlopen(req1,timeout = 5)
    except urllib.error.URLError as e:
        L.append(e.reason)
        print(L)
        return L
    except Exception as ex:
        L.append(str(ex))
        print(L)
        return L

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

    try:
        response2 = urllib.request.urlopen(req2,timeout = 5)
    except urllib.error.URLError as e:
        L.append(e.reason)
        print(L)
        return L
    except Exception as ex:
        L.append(str(ex))
        print(L)
        return L
        
    result2 = response2.read().decode()
    result2 = json.loads(result2)    
    if(result2['status'] != 'ok'):
        L.append('FAILED')
        print(L)
        return L
    else:
        L.append('OK')
        i=1
        Lvalue=[]
        for string in result2['ret'] :
            if( i > 3  or string[0]=='DESC' ):
                break
            flag = 0
            for value in Lvalue:
                if(string[1]==value):
                    flag = 1
                    break 
            if(flag):
                continue
            Lvalue.append(string[1])
            L.append(string[1])
            i=i+1
        print(L)
        return L
    #        return(result['ret'])
st = input()
getproperty(st)