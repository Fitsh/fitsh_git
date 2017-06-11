#-*- encoding:utf8-*-
import re
import requests
from pprint import pprint

url ="https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9013"
r = requests.get(url,verify=False)
stations = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)',r.text)
tmp={}
stations=dict(stations)
stations_rev={}
for k,v in stations.items():
	k=k.encode('UTF-8')
	v=v.encode('UTF-8')
	tmp[k]=v
	stations_rev[v]=k
pprint(tmp,indent=4)
pprint(stations_rev,indent=4)
