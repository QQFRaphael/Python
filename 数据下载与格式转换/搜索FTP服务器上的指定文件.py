#!/usr/bin/python
# QQF @ 2023-07-12
# this script check the WARRS and WARMS files in 154 and 179 server
# example: ./check-ftp --time=2023
# example: ./check-ftp --time=202307
# example: ./check-ftp --time=20230708
# example: ./check-ftp --time=2023070800
import argparse
from ftplib import FTP

parser = argparse.ArgumentParser(description="check files in 154 and 179 ftp server, example: python this.py --time=20230701")
parser.add_argument("--time", type=str, help="input the day you want to check")

args = parser.parse_args()
time = str(args.time)

print("=========================== CHECK 10.135.30.154 SERVER ===========================")
# check 154 FTP
print("connecting 154 server...")
ftp = FTP("10.135.30.154")
print("login 154 server...")
ftp.login("kys","kys123")
print("find data dir...")
ftp.cwd('/ZJWARRS/DATA_HISTORY/%s' % (time[0:4]))
print("get files")
allfiles = ftp.nlst()
print("search target files")
print("------------------- 154 server target WARRS files -------------------")
for f in allfiles:
	if time in f: 
		print("%s: %4.2fG" % (f,ftp.size(f)/1024./1024./1024.))
print("------------------- 154 server target WARMS files -------------------")
ftp.cwd('/ZJWARMS/DATA_HISTORY/%s' % (time[0:4]))
allfiles = ftp.nlst()
for f in allfiles:
        if time in f:
		print("%s: %4.2fG" % (f,ftp.size(f)/1024./1024./1024.))


print("=========================== CHECK 10.135.30.179 SERVER ===========================")
# check 179 FTP
print("connecting 179 server...")
ftp = FTP("10.135.30.179")
print("login 179 server...")
ftp.login("sqksuser","sqksuser")
print("find data dir...")
ftp.cwd('/realtimedata/nafp/ZJWARRS/nc')
print("get files")
allfiles = ftp.nlst()
print("search target files")
print("------------------- 179 server target WARRS files -------------------")
for f in allfiles:
	if time in f: 
		print("%s: %4.2fG" % (f,ftp.size(f)/1024./1024./1024.))
print("------------------- 179 server target WARMS files -------------------")
ftp.cwd('/realtimedata/nafp/ZJWARMS/nc')
allfiles = ftp.nlst()
for f in allfiles:
        if time in f:
                print("%s: %4.2fG" % (f,ftp.size(f)/1024./1024./1024.))
