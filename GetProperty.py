# -*- coding utf-8 -*-
import urllib
import urllib.request
import json
get = input()
url = "http://shuyantech.com/api/cndbpedia/avpair?q="+urllib.parse.quote(get)  
req = urllib.request.Request(url)
response = urllib.request.urlopen(req)

result = response.read().decode()
print(type(result))
result = json.loads(result)

if(result['status'] != 'ok'):
#    return
    pass
else:
    for string in result['ret'] :
        print(string)
#        return(result['ret'])


