# -*- coding utf-8 -*-
import urllib
import urllib.request
import urllib.error
import json
def getproperty(sta):
    L=[]    #返回用的list
    sta = str.lower(sta) #根据接口要求将输入字母调整为全小写
    url1 = "http://shuyantech.com/api/cndbpedia/ment2ent?q="+urllib.parse.quote(sta)  
    req1 = urllib.request.Request(url1)
# 以原命名为基础检索数据库相关条目，若超时/无网络等情况则返回错误情况，无条目返回no label，访问失败返回failed
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
#将检索到的权值最高的条目视作目标，再次访问数据库获得label，返回值情况与上述相同
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
    else:               #成功之后list首项为ok，之后为最多3项的目标属性
        L.append('OK')
        i=1
        Lvalue=[]
        for string in result2['ret'] :
            if( i > 3  or string[0]=='DESC' ):
                break
            flag = 0
            for value in Lvalue:
                if(string[1]==value):#避免出现相同属性
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
#st = input()
#getproperty(st)