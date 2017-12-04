#!/usr/local/bin/pyenv python
# Created by carrot at 2017/9/10

# -*- coding=utf-8 -*-

"""
从天天开奖网获取数据
https://1680660.com/smallSix/findSmallSixHistory.do?year=2017&type=1
"""

import requests
import json
from . import dbconnection
import datetime


class LotteryObj(object):
	def __init__(self, data):
		self.nanairo = data.get("nanairo")
		self.seventhCompositeDouble = data.get("seventhCompositeDouble")
		self.seventhCompositeBig = data.get("seventhCompositeBig")
		self.seventhMantissaBig = data.get("seventhMantissaBig")
		self.color = data.get("color")
		self.issue = data.get("issue")
		self.seventhSingleDouble = data.get("seventhSingleDouble")
		self.seventhBigSmall = data.get("seventhBigSmall")
		self.totalBigSmall = data.get("totalBigSmall")
		self.totalSingleDouble = data.get("totalSingleDouble")
		self.preDrawDate = data.get("preDrawDate")
		self.preDrawCode = data.get("preDrawCode")
		self.sumTotal = data.get("sumTotal")
		self.czAndFeSeven = data.get("czAndFeSeven")
		self.__handlerdata()

	def __handlerdata(self):
		self.issueSerial = int(self.issue)
		# datas = [x for x in self.preDrawCode.split(",")]
		self.issueNums = [int(x) for x in self.preDrawCode.split(",")]
		# self.issueData = datetime.datetime.strptime(self.preDrawDate, "%Y-%m-%d")
		self.issueDate = self.preDrawDate
		self.issueYear = datetime.datetime.strptime(self.preDrawDate, "%Y-%m-%d").year
		# print(self.issueDate)

	def __unicode__(self):
		result = "%03d\t\t" % (int(self.issue),)
		nums = self.preDrawCode.split(",")
		for num in nums:
			result += ("%02d " % (int(num),))
		return result

	def __str__(self):
		return self.__unicode__()

	def sel_sql(self):
		sel_sql = 'select * from t_lottery_record where seq = %d and pub_date = "%s" and year=%d' % (self.issueSerial, self.issueDate, self.issueYear)
		print("sel_sql:%s" % (sel_sql,))
		return sel_sql

	def ins_sql(self):
		ins_sql = 'insert into t_lottery_record (seq,num1,num2,num3,num4,num5,num6,specnum,pub_date,year) value(%d, %d, %d,%d,%d,%d,%d,%d,"%s",%d)' % (self.issueSerial, self.issueNums[0], self.issueNums[1], self.issueNums[2], self.issueNums[3], self.issueNums[4], self.issueNums[5], self.issueNums[6], self.issueDate, self.issueYear)
		return ins_sql

	def up_sql(self):
		up_sql = 'update t_lottery_record set num1=%d,num2=%d,num3=%d,num4=%d,num5=%d,num6=%d,specnum=%d where seq=%d and pub_date="%s" and year=%d' % (self.issueNums[0], self.issueNums[1], self.issueNums[2], self.issueNums[3], self.issueNums[4], self.issueNums[5], self.issueNums[6], self.issueSerial, self.issueDate, self.issueYear)
		return up_sql


class LotteryData(object):
	def __init__(self, data):
		self.errorCode = data.get("errorCode")
		self.message = data.get("message")
		self.errorCode = data.get("errorCode")
		self.errorCode = data.get("errorCode")
		listdata = data.get("result").get("data").get("bodyList")
		self.list = []
		for item in listdata:
			self.list.append(LotteryObj(item))

	def __unicode__(self):
		result = ""
		for item in self.list:
			result += str(item) + "\n"
		return result

	def __str__(self):
		return self.__unicode__()

	@staticmethod
	def storage(lists):
		print(dbconnection.dbcon)
		cur = dbconnection.dbcon.cursor()
		for item in lists:
			effect_row = cur.execute(item.sel_sql())
			if effect_row:
				cur.execute(item.up_sql())
			else:
				cur.execute(item.ins_sql())
		dbconnection.dbcon.commit()
		cur.close()

	@staticmethod
	def query():
		cur = dbconnection.dbcon.cursor()
		cur.execute('select * from t_lottery_record order by year desc, seq DESC')
		return cur.fetchall()


def start():
	collests = {}
	datas = []
	for idx in range(2003, 2018):
		payload = {"year": idx, "type": 1}
		r = requests.post('https://1680660.com/smallSix/findSmallSixHistory.do', data=payload)
		data = json.loads(r.text)
		result = LotteryData(data)
		# print("%d\n%s" % (idx, result))
		collests["%d" % (idx,)] = result
		# datas.extend(result.list)
		datas = datas + result.list
	LotteryData.storage(datas)
	return collests


def query():
	LotteryData.query()


def statisticsresult1():
	result = [{}, {}]
	for i in range(1, 50):
		result[0][i] = [0, 0]
		result[1][i] = [0, 0]
	datas = LotteryData.query()
	for item in datas:
		for index in range(2, 8):
			result[0][item[index]][0] = result[0][item[index]][0] + 1
		result[1][item[8]][0] = result[1][item[8]][0] + 1
	for i in range(1, 50):
		result[0][i][1] = int(result[0][i][0] / len(datas) * 10000) / 100
		result[1][i][1] = int(result[0][i][0] / len(datas) * 10000) / 100
	return json.dumps(result)


def statisticsresult2():
	result = [{}, {}]
	for i in range(1, 50):
		result[0][i] = [0, 0]
		result[1][i] = [0, 0]
	datas = LotteryData.query()
	for item in datas:
		for index in range(2, 9):
			result[0][item[index]][0] = result[0][item[index]][0] + 1
		result[1][item[8]][0] = result[1][item[8]][0] + 1
	for i in range(1, 50):
		result[0][i][1] = int(result[0][i][0] / len(datas) * 10000) / 100
		result[1][i][1] = int(result[1][i][0] / len(datas) * 10000) / 100
	return json.dumps(result)


class NumCounter(object):
	def __init__(self, num, count=0, rate=0):
		self.num = num
		self.count = count
		self.rate = rate


# 重写JSONEncoder的default方法，object转换成dict
class NumCounterEncoder(json.JSONEncoder):
	def default(self, o):
		if isinstance(o, NumCounter):
			return {
				'num': o.num,
				'count': o.count,
				'rate': o.rate,
			}
		return json.JSONEncoder.default(o)


# 重写JSONDecoder的decode方法，dict转换成object
class NumCounterDecode(json.JSONDecoder):
	def decode(self, s):
		dic = super().decode(s)
		return NumCounter(dic['num'], dic['count'], dic['rate'])


# 重写JSONDecoder的__init__方法，dict转换成object
class NumCounterDecode(json.JSONDecoder):
	def __init__(self):
		json.JSONDecoder.__init__(self, object_hook=dic2objhook)


# 对象转换成dict
def obj2dict(obj):
	if isinstance(obj, NumCounter):
		return {'num': obj.num, 'count': obj.count, 'rate': obj.rate}
	else:
		return obj


# dict转换为对象
def dic2objhook(dic):
	if isinstance(dic, dict):
		return NumCounter(dic['num'], dic['count'], dic['rate'])
	return dic



def statisticsresult3():
	result = [[], []]
	for i in range(0, 50):
		result[0].append(NumCounter(i))
		result[1].append(NumCounter(i))
	datas = LotteryData.query()
	for item in datas:
		for index in range(2, 9):
			# result[0][item[index]][0] = result[0][item[index]][0] + 1
			countObjNormal = result[0][item[index]]
			countObjNormal.count = countObjNormal.count + 1
		# result[1][item[8]][0] = result[1][item[8]][0] + 1
		countObjSpec = result[1][item[8]]
		countObjSpec.count = countObjSpec.count + 1
	for i in range(1, 50):
		# result[0][i][1] = int(result[0][i][0] / len(datas) * 10000) / 100
		# result[1][i][1] = int(result[1][i][0] / len(datas) * 10000) / 100
		countObjNormal = result[0][i]
		countObjNormal.rate = int(countObjNormal.count / len(datas) / 7 * 10000) / 100
		countObjSpec = result[1][i]
		countObjSpec.rate = int(countObjSpec.count / len(datas) / 7 * 10000) / 100
	# return json.dumps(result, default=obj2dict)
	# return json.dumps(result, cls=NumCounterEncoder)
	return result

def main():
	pass


if __name__ == "__main__":
	main()

