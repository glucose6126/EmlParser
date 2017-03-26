#Eml Parser
import os
import re
import time
import email as emailModule
import urllib
import sqlite3
import hashlib
import datetime

def getTime(varTime) : #parsing Time regex data
	#Thu, 16 Feb 2017 01:44:59 -0800 (PST) Time format
	monthDic = {
				'Jan' : 1,
				'Feb' : 2,
				'Mar' : 3,
				'Apr' : 4,
				'May' : 5,
				'Jun' : 6,
				'Jul' : 7,
				'Aug' : 8,
				'Sep' : 9,
				'Oct' : 10,
				'Nov' : 11,
				'Dec' : 12
				}
	timeSet = varTime.split(' ')
	datetimeSet = {}
	datetimeSet['year'] = timeSet[3]
	datetimeSet['month'] = monthDic[timeSet[2].replace(',', '')]
	datetimeSet['day'] = timeSet[1]
	datetimeSet['time'] = timeSet[4]
	datetimeSet['timezone'] = calcTime(timeSet[5])
	s = datetimeSet['year'] + "/" + str(datetimeSet['month']) + "/" + datetimeSet['day'] + " " + datetimeSet["time"]
	try:
		timestamp = time.mktime(datetime.datetime.strptime(s, "%Y/%m/%d %H:%M:%S").timetuple()) + datetimeSet['timezone']
	except :
		print "[!] Error"
		# print varTime
		# print datetimeSet
	return timestamp

def calcTime(timezone) : #calc Time zone to UTC+0
	#timeZone
	plmaDic = {"+" : 1, "-" : -1}
	timezone_plma   = plmaDic[timezone[0]]
	timezone_hour   = timezone[-4:-2]
	timezone_minute = timezone[-2:]

	timezone_summary = (timezone_plma * ((int(timezone_hour) * 60) + int(timezone_minute))) * 60
	return timezone_summary
	#Todo : add Time to UTC +0 Calculation CODE

def decodeToFrom(data) :
	# To: "=?euc-kr?B?sejBvsf2tNQ=?=" <joseph@duzon.com>
	if len(data.split("\"")) != 1 :
		name = data.split("\"")[1]
	else :
		name = ''

	if len(data.split('<')) != 1 :
		email = data.split('<')[1].split('>')[0]
	else :
		email = data.split('To: ')[1]

	if len(name.split('?')) == 5 :
		# ['=', 'euc-kr', 'B', 'sejBvsf2tNQ=', '=']
		charencode = name.split('?')[1] #euc-kr
		encode     = name.split('?')[2] #B
		encoded    = name.split('?')[3] #sejBvsf2tNQ

		if encode == 'B' :
			encoded = encoded.decode('base64')
		elif encode == 'Q' :
			encoded = urllib.unquote(encoded.replace('=', '%'))

		try :
			if charencode.lower() == 'euc-kr':
				encoded = encoded.decode('euc-kr')
				# print type(encoded), 'eeee'
			elif charencode.lower() == 'utf-8':
				encoded = encoded.decode('utf-8')
				# print encoded

		except :
			print "Decoded Error : " + data
			print "Now : " + encoded

	else : #Not Encoded
		encoded = name

	return encoded, email

def decodeSubject(data) :
	# Subject: Sept 30th: Learn How Moving your Contact Center to the Cloud Eliminates Risk
	# Subject: =?EUC-KR?B?SVNFQyAyMDE0v6Egv6m3r7rQwLsgw8q068fVtM+02SE=?=
	data = data.replace('Subject: ', '')

	if len(data.split('?')) >= 5 :
		if len(data.split(' ')) != 1 :
			subject = ''
			for i in data.split(' ') :
				subject = subject + decodeSubject(i) + ' '
			return subject[:-1]

		# ['=', 'euc-kr', 'B', 'sejBvsf2tNQ=', '=']
		charencode = data.split('?')[1] #euc-kr
		encode     = data.split('?')[2] #B
		encoded    = data.split('?')[3] #sejBvsf2tNQ

		if encode == 'B' :
			encoded = encoded.decode('base64')
		elif encode == 'Q' :
			encoded = urllib.unquote(encoded.replace('=', '%'))

		try :
			if charencode.lower() == 'euc-kr':
				encoded = encoded.decode('euc-kr')
				# print type(encoded), 'eeee'
			elif charencode.lower() == 'utf-8':
				encoded = encoded.decode('utf-8')
				# print encoded
			elif charencode.lower() == 'gbk' :
				encoded = encoded.decode('GBK')

		except :
			print "Decoded Error : " + data
			print "Now : " + encoded
			print "Data : ", data

	else : #Not Encoded
		encoded = data.replace('Subject: ', '')

	return encoded

def decodeFilename(data) :
	# Subject: Sept 30th: Learn How Moving your Contact Center to the Cloud Eliminates Risk
	# Subject: =?EUC-KR?B?SVNFQyAyMDE0v6Egv6m3r7rQwLsgw8q068fVtM+02SE=?=
	if len(data.split('\n')) != 1 :
		res = ''
		for i in data.split('\n') :
			res = res + decodeFilename(i) + ' '
		res = res[:-1]
		return res

	else :
		if len(data.split('?')) == 5 :
			# ['=', 'euc-kr', 'B', 'sejBvsf2tNQ=', '=']
			charencode = data.split('?')[1] #euc-kr
			encode     = data.split('?')[2] #B
			encoded    = data.split('?')[3] #sejBvsf2tNQ

			if encode == 'B' :
				encoded = encoded.decode('base64')
			elif encode == 'Q' :
				encoded = urllib.unquote(encoded.replace('=', '%'))

			try :
				if charencode.lower() == 'euc-kr':
					encoded = encoded.decode('euc-kr')
					# print type(encoded), 'eeee'
				elif charencode.lower() == 'utf-8':
					encoded = encoded.decode('utf-8')
					# print encoded
				elif charencode.lower() == 'gbk' :
					encoded = encoded.decode('GBK')

			except :
				print "Decoded Error : " + data
				print "Now : " + encoded
				print "Data : ", data

		else : #Not Encoded
			encoded = data

	return encoded

def decodeFile(data) :
	if len(re.findall('[A-Za-z0-9+/=\n]+', data.replace('!\n ', ''))) == 1 :
		return data.replace('!\n ', '').decode('base64')
	if len(re.findall('[A-Za-z0-9+/=\n]+', data)) == 1 :
		if data == re.findall('[A-Za-z0-9+/=\n]+', data)[0] :
			return data.decode('base64')
	elif len(data.split('=\n')) > 2:
		data = urllib.unquote(data.replace('=\n', '').replace('=', '%'))
		# print "Changed"
	return data

def decodeContent(data) :
	if len(re.findall('[A-Za-z0-9+/=\n! ]+', data)) == 1 :
		if data.replace('!\n ', '') == re.findall('[A-Za-z0-9+/=\n]+', data.replace('!\n ', ''))[0] :
			return data.replace('!\n ', '').decode('base64')
	else :
		return data

def get_attach(msg, filename, filenumber, output_directory, cur) :
	if msg.is_multipart() == True :
		for msgpart in msg.get_payload() :
			get_attach(msgpart, filenumber, filenumber, output_directory, cur)
	else :
		file     = decodeFile(msg.get_payload())
		filename = msg.get_filename()
		filememe = msg.get_content_maintype()
		md5      = hashlib.md5(file).hexdigest()
		sha256   = hashlib.sha256(file).hexdigest()

		if filename == None :
			filename = 'Noname-' + md5

		filename = decodeFilename(filename)

		if not os.path.exists(output_directory + '/' + str(filenumber)) :
			os.makedirs(output_directory + '/' + str(filenumber))	

		if msg.get_content_type() == 'text/html' :
			filename = 'EMLParser_content.html'
			global content
			content = file
			# print "[!] FILE UPDATE"

		elif msg.get_content_type() == 'text/plain' :
			filename = 'EMLParser_content-' + md5 + '.txt'

		ext = filename.split('.')[-1]
		cur.execute("insert into attach(emlNumber, filename, ext, filememe, md5, sha256) values(?,?,?,?,?,?)", (filenumber, filename, ext, filememe, md5, sha256))
		open(output_directory + '/' + str(filenumber) + '/' + filename, 'wb').write(file)
		# print msg.get_payload()


def emlparser(filelist) :
	now = time.strftime("%Y_%m_%d_%H_%M_%S", time.gmtime())
	conn = sqlite3.connect(now + '.db')
	conn.text_factory = str
	cur = conn.cursor()

	output_directory = './' + now + '_output'

	if not os.path.exists(output_directory) :
		os.makedirs(output_directory)

	try :
		cur.execute("create table data(lid int AUTO_INCREMENT PRIMARY KEY, \
									   filelocation char(255) NOT NULL, \
									   filename char(255) NOT NULL, \
									   sendTime int NOT NULL, \
									   recvTime int NOT NULL, \
									   sendID char(255), \
									   sendName char(255), \
									   recvID char(255), \
									   recvName char(255), \
									   subject TEXT, \
									   content TEXT, \
									   md5 char(255), \
									   sha256 char(255))")
	except :
		pass

	try :
		cur.execute("create table attach(lid INTEGER PRIMARY KEY,\
					 emlNumber int NOT NULL, \
					 filename char(255), \
					 ext char(255), \
					 filememe char(255), \
					 md5 char(255) NOT NULL, \
					 sha256 char(255) NOT NULL)")
	except :
		pass

	conn.commit()
	filenumber = 0
	for filename in filelist :
		filenumber = filenumber + 1
		print "[+] File : " + filename
		file    = open(filename, 'rb').read()
		md5 = hashlib.md5(file).hexdigest()
		sha256 = hashlib.sha256(file).hexdigest()
		header  = file.split('\x0d\x0a\x0d\x0a')[0]
		tmp_content = file.split('\x0d\x0a\x0d\x0a')[1:]
		
		global content
		content = ''
		for i in tmp_content :
			content = content + i + '\x0d\x0a\x0d\x0a'
		content = content[:-4]

		content = decodeContent(content)

		try :
			sender  = re.findall('\nTo: .+\n', header)[0].replace('\n', '').replace('\r', '')
			reciver = re.findall('\nFrom: .+\n', header)[0].replace('\n', '').replace('\r', '')
			# print sender
			sender, senderName = decodeToFrom(sender)
			# print reciver
			reciver, reciverName = decodeToFrom(reciver)

		except :
			print "[!] Mail Address Parsing Error"
			# print header
			os.system("pause")

		try :
			subject = re.findall('\nSubject: .+\n', header)[0].replace('\n', '').replace('\r', '')
			subject = decodeSubject(subject)
			# print subject
		except :
			print "[!] Mail Subject Parsing Error"
			# print header
			os.system("pause")

		reTime = '((Mon|Tue|Wed|Thu|Fri|Sat|Sun), [0-3][0-9] (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Dec|Oct|Sep|Nov) [1-2][0-9]{3} [0-2][0-9]:[0-5][0-9]:[0-5][0-9] [+,-][0-9]{4})'
		sendTime = re.findall(reTime, header)
		timeSet = []
		for i in sendTime :
			timeSet.append(getTime(i[0]))
		timeSet.sort()
		SendTime = timeSet[0]
		# print SendTime
		RecvTime = timeSet[-1]
		# print RecvTime

		# if(len(header.split("boundary")) >= 2) :
		# 	# print "[!]" + `len(header.split("boundary"))`
		# 	boundary = re.findall("boundary=\".+\"", header)[0]
		# 	print boundary
		# 	# os.system("pause")
		# 	for i in content.split(boundary.replace('--', '')) :
		# 		print i
		# 		os.system('pause')

		# if(len(header.split("Content-Transfer-Encoding")) >= 2):
		# 	# print len(header.split("Content-Transfer-Encoding"))
		# 	print re.findall("Content-Transfer-Encoding: .+\n", header)[0]
		# 	os.system("pause")
		# print "=" * 50

		msg = emailModule.message_from_file(open(filename))
		
		get_attach(msg, filename, filenumber, output_directory, cur)
		conn.commit()

		# if msg.is_multipart() == True :	#seperate data
		# 	for part in msg.get_payload() :
		# 		#functionalization

		# else : #
		# 	content = msg.get_payload()
			
		# print content
		cur.execute("insert into data(lid, sendTime, recvTime, recvID, recvName, sendID, sendName, subject, content, filelocation, filename, md5, sha256) values(?,?,?,?,?,?,?,?,?,?,?,?,?)", (filenumber, SendTime, RecvTime, senderName, sender, reciverName, reciver, subject, content, filename, filename.split('/')[-1], md5, sha256))

	conn.commit()

		# From: =?utf-8?Q?Israel=20Homeland=20Security=20=28iHLS=29?= <info@i-hls.com> Sender
		# To: =?utf-8?Q?Joseph?= <joseph@duzon.com> Reciver
		# Subject: =?utf-8?Q?Military=20and=20C4I=20Technologies=20For=20Terrain=20Dominance=20Conference?=
		# Date: Tue, 8 Dec 2015 14:53:45 +0000 Recive Time recive Time
		# recvDate: Tue, 08 Dec 2015 23:51:23 +0900 sendTime
		# recived : low ==> sender, high ==> reciver
	return now + '.db'