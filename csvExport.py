import sqlite3
import sys

dbname = sys.argv[1]
# dbname = "2017_03_16_09_09_49.db"
conn = sqlite3.connect(dbname)
conn.text_factory = str
cur  = conn.cursor()
cur.execute("select * from data")
datas = cur.fetchall()
outputFile = open(dbname.split('.')[0] + "-data.csv", 'wb')
outputFile.write("\xEF\xBB\xBF")
outputFile.write("lid,filelocation,filename,SendTime,recvTime,sendID,sendName,recvID,recvName,subject,content,md5,sha256\r\n")
for data in datas :
	outputFile.write(str(data[0]) + ",")
	outputFile.write(str(data[1]) + ",")
	outputFile.write(str(data[2]) + ",")
	outputFile.write(str(data[3]) + ",")
	outputFile.write(str(data[4]) + ",")
	outputFile.write(str(data[5]) + ",")
	outputFile.write(str(data[6]) + ",")
	outputFile.write(str(data[7]) + ",")
	outputFile.write(str(data[8]) + ",")
	outputFile.write(str(data[9]) + ",")
	outputFile.write(str(data[10]).replace(',', '').replace('\n', '').replace('\t', '').replace('\n', '').replace(';', '').replace('\x0d', '')+ ", ")
	outputFile.write(str(data[11]) + ", ")
	outputFile.write(str(data[12]) + "\r\n")

outputFile.write("\xEF\xBB\xBF")
outputFile = open(dbname.split('.')[0] + "-attachFile.csv", 'wb')
outputFile.write("lid, emlNumber, filename, ext, filememe, md5, sha256\r\n")
cur.execute("select * from attach")
datas = cur.fetchall()
for data in datas :
	outputFile.write(str(data[0]) + ",")
	outputFile.write(str(data[1]) + ",")
	outputFile.write(str(data[2]) + ",")
	outputFile.write(str(data[3]) + ",")
	outputFile.write(str(data[4]) + ",")
	outputFile.write(str(data[5]) + ",")
	outputFile.write(str(data[6]) + "\r\n")