#-*- encoding:utf8 -*-
import itchat
import requests

url='http://www.tuling123.com/openapi/api'
key='f7738f6d2cce4e2aae6277f42e9efd41'
def reply(response,fromusername):
	response=response.json()
#	print response
	if response['code'] == 100000:
		itchat.send(response['text'],fromusername)
	elif response['code'] == 200000:
		itchat.send(response['url']+response['text'],fromusername)
	elif response['code'] == 302000:
		itchat.send(response['text']+'\n'
				+ response['list']['article']+'\n'
				+response['list']['icon']+response['list']['detailurl'],
				fromusername)
	elif response['code'] == 308000:
		itchat.send(response['text']+'\n'
				+ response['list']['name']+'\n'
				+ response['list']['info']+'\n'
				+response['list']['icon']+response['list']['detailurl'],
				fromusername)
	elif response['code'] == 313000:
		itchat.send(response['text']+'\n'
				+ response['function']['song']+'\n'
				+response['function']['singer'],
				fromusername)
	elif response['code'] == 314000:
		itchat.send(response['text']+'\n'
				+ response['function']['author']+'\n'
				+response['function']['name'],
				fromusername)

@itchat.msg_register(itchat.content.TEXT)
def print_content(msg):
#	print msg['Text']
	ms={'key':key,
		'info':msg['Text'],
		'userid':msg['FromUserName']
	}
	r = requests.post(url,ms)
	reply(r, msg['FromUserName'])

itchat.auto_login(hotReload=True)
itchat.run()
itchat.send('测试消息发送'.decode('utf-8'),'filehelper')
