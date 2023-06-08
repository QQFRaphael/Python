import os
import time
import datetime
import calendar
import requests
import multiprocessing

def add_months(dt, months):
	month = dt.month - 1 + months
	year = dt.year + month // 12
	month = month % 12 + 1
	day = min(dt.day, calendar.monthrange(year, month)[1])
	return dt.replace(year=year, month=month, day=day)

def download(args):
	url_heads = args[0]
	dirname = args[1]
	filenames = args[2]

	for eachfile in filenames:
		url = "%s%s/%s" % (url_heads, dirname, eachfile)
		flag = True
	
		while flag:
			try:
				myrequest = requests.get(url, timeout=60)
				if myrequest.ok:
					with open("%s/%s" % (dirname, eachfile), "wb") as f:
						f.write(myrequest.content)
					print("%s/%s is downloaded" % (dirname, eachfile))
				myrequest.close()
				time.sleep(3)
				flag = False
			except requests.exceptions.RequestException as e:
				print(e)
				print("%s/%s will try again........" % (dirname, eachfile))
				time.sleep(15)

heads = "flxf.01."
tails = ".avrg.grib.grb2"
url_heads = "https://www.ncei.noaa.gov/data/climate-forecast-system/access/operational-9-month-forecast/monthly-means/"

if __name__ == "__main__":
	pool = multiprocessing.Pool(processes=6)

	for year in range(2016,2023):
		for mon in range(1,13):
			for day in range(1,calendar.mdays[mon]+1):
				monstr = str(mon).zfill(2)
				daystr = str(day).zfill(2)
				dt = datetime.datetime.strptime("%s-%s" % (year, mon), "%Y-%m")
	
				# 9 months forecast, sometimes include the current
				month_list = ["%s%s" % (year, monstr)]
				for idx in range(1, 9+1):
					month_list.append(add_months(dt,int(idx)).strftime("%Y%m"))
	
				for hour in ['00','06','12','18']:	
					current = "%s%s%s%s" % (year, monstr, daystr, hour)
	
					filenames = []
					for eachfile in month_list:
						filename = "%s%s.%s%s" % (heads, current, eachfile, tails)
						filenames.append(filename)
	
					# create folder
					dirname = "%s/%s%s/%s%s%s/%s%s%s%s" % (year, year, monstr, year, monstr, daystr, year, monstr, daystr, hour)
					if not os.path.exists(dirname): os.makedirs(dirname)
	
					# download file
					myargs = (url_heads, dirname, filenames)
					pool.apply_async(download, args=(myargs,))
	pool.close()
	pool.join()