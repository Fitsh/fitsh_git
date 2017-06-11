#-*- encoding: utf8 -*-

"""命令行火车票查看器

Usage:
	tickets [-gdtkz] <from> <to> <date>

Options:
	-h,--help	显示帮助菜单
	-g			高铁
	-d			动车
	-t			特快
	-k			快速
	-z			直达

Example:
	tickets 北京 上海 2016-10-10
	tickets -dg 成都 南京 2016-10-10
"""
from docopt import docopt
from stations import stations,stations_rev
import requests
from prettytable import PrettyTable
from colorama import init,Fore
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class TrainsCollection:
	
	header='车次 车站 时间 历时 一等 二等 软卧 硬卧 软座 硬座 无座'.split()
	
	def __init__(self,available_trains, options):
		"""查询到的火车集合

			:param available_trains: 一个列表，包含可获的火车班次，每个
									火车班次是一个列表
			:param options:查询的选项，如高铁，动车，etc...
		"""
		self.available_trains = available_trains
		self.options=options
	
	def _get_duration(self,raw_train):
		duration = raw_train[10].encode('utf-8').replace(':','小时')+'分'
		if duration.startswith('00'):
			return duration[4:]
		if duration.startswith('0'):
			return duration[1:]
		return duration

	def trains(self):
		for raw_train in self.available_trains:
			raw_train = raw_train.split('|')
			train_no = raw_train[3]
			inintial = train_no[0].lower()
			if not self.options or inintial in self.options:
				train=[
					train_no,
					'\n'.join([Fore.GREEN + stations_rev.get(raw_train[6]) + Fore.RESET,
							Fore.RED+stations_rev.get(raw_train[7])+Fore.RESET]),
					'\n'.join([Fore.GREEN+raw_train[8]+Fore.RESET,
							Fore.RED+raw_train[9]+Fore.RESET]),
					self._get_duration(raw_train),
					raw_train[31] if raw_train[31] !='' else '--',
					raw_train[30] if raw_train[30] != '' else '--',
					raw_train[23] if raw_train[23] != '' else '--',
					raw_train[28] if raw_train[28] != '' else '--',
					raw_train[27] if raw_train[27] != '' else '--',
					raw_train[29] if raw_train[29] != '' else '--',
					raw_train[26] if raw_train[26] != '' else '--',
				]
				yield train
	
	def pretty_print(self):
		pt = PrettyTable()
		pt._set_field_names(self.header)
		for train in self.trains():
			pt.add_row(train)
		print pt


def cli():
	"""command-line interface"""
	arguments = docopt(__doc__,help=True,version=None)
	from_station = stations.get(arguments['<from>'])
	to_station = stations.get(arguments['<to>'])
	date = arguments['<date>']
#	url1='https://kyfw.12306.cn/otn/leftTicket/log?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(date, from_station, to_station)
#	rr = requests.get(url1,verify=False)
#	print rr.text
	url='https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(
	date, from_station, to_station
	)

	options = ''.join([ key for key,value in arguments.items() if value is True])

	r = requests.get(url, verify=False)
	if r.json() is None or 'data' not in r.json():
		print 'No information'
		return 
	available_trains= r.json()['data']['result']
#	i = 0
#	for s in available_trains[1].split('|'):
#		if isinstance(s,unicode):
#			print i,s.encode('utf-8')
#		else:
#			print i,s
#		i+=1
	TrainsCollection(available_trains, options).pretty_print()
if __name__== '__main__':
	init()
	cli()
