import os
import time
import datetime
import calendar
import requests

def add_months(dt, months):
    month = dt.month - 1 + months
    year = dt.year + month // 12
    month = month % 12 + 1
    day = min(dt.day, calendar.monthrange(year, month)[1])
    return dt.replace(year=year, month=month, day=day)

heads = "flxf.01."
tails = ".avrg.grib.grb2"
url_heads = "https://www.ncei.noaa.gov/data/climate-forecast-system/access/operational-9-month-forecast/monthly-means/"

for year in range(2012,2023):
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
				for eachfile in filenames:
					url = "%s%s/%s" % (url_heads, dirname, eachfile)
					
					myrequest = requests.get(url)
					time.sleep(1)

					if myrequest.ok:
						with open("%s/%s" % (dirname, eachfile), "wb") as f:
							f.write(myrequest.content)
						print("%s/%s is downloaded" % (dirname, eachfile))
					myrequest.close()
					time.sleep(5)