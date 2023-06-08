import os
import time
import requests
import multiprocessing

# this script download the NOAA NCEP II daily files
year_start = 1979
year_end = 2023


filetails = "nc"

surface = ['mslp', 'pres.sfc', 'pr_wtr.eatm', 'land', 'hgt.sfc']
pressure = ['air', 'hgt', 'omega', 'rhum', 'uwnd', 'vwnd']
gaussian_grid = ["air.2m.gauss", "cprat.sfc.gauss", "dlwrf.sfc.gauss", "dswrf.ntat.gauss", "dswrf.sfc.gauss", "gflux.sfc.gauss", "hgt.sfc.gauss", "icec.sfc.gauss", "land.sfc.gauss", "lhtfl.sfc.gauss", "pevpr.sfc.gauss", "prate.sfc.gauss", "pres.hcb.gauss", "pres.hct.gauss", "pres.lcb.gauss", "pres.lct.gauss", "pres.mcb.gauss", "pres.mct.gauss", "pres.sfc.gauss", "runof.sfc.gauss", "shtfl.sfc.gauss", "shum.2m.gauss", "skt.sfc.gauss", "soilw.0-10cm.gauss", "soilw.10-200cm.gauss", "tcdc.eatm.gauss", "tmax.2m.gauss", "tmin.2m.gauss", "tmp.0-10cm.gauss", "tmp.10-200cm.gauss", "uflx.sfc.gauss", "ugwd.sfc.gauss", "ulwrf.ntat.gauss", "ulwrf.sfc.gauss", "uswrf.ntat.gauss", "uswrf.sfc.gauss", "uwnd.10m.gauss", "vflx.sfc.gauss", "vgwd.sfc.gauss", "vwnd.10m.gauss", "weasd.sfc.gauss"]

dirnames = {
	'surface': surface,
	'pressure': pressure,
	'gaussian_grid': gaussian_grid
}

url_heads = "https://downloads.psl.noaa.gov/Datasets/ncep.reanalysis2/Dailies/"

def download(args):
	filepath = args[0]
	url = args[1]

	flag = True
	while flag:
		try:
			myrequest = requests.get(url, timeout=60)

			if myrequest.ok:
				with open(filepath, "wb") as f:
					f.write(myrequest.content)
				print("%s is downloaded" % filepath)
			myrequest.close()
			time.sleep(3)
			flag = False
		except requests.exceptions.RequestException as e:
			print(e)
			print("%s will try again......" % filepath)


if __name__ == "__main__":
	pool = multiprocessing.Pool(processes=6)

	for dirname in dirnames.keys():
		if not os.path.exists(dirname): os.makedirs(dirname)

		for var in dirnames[dirname]:
			if var not in ['land', 'hgt.sfc', 'hgt.sfc.gauss', 'land.sfc.gauss']:
				for year in range(year_start, year_end+1):
					filename = "%s.%s.%s" % (var, year, filetails)
					filepath = "%s/%s.%s.%s" % (dirname, var, year, filetails)
					url = "%s%s" % (url_heads, filepath)

					myargs = (filepath, url)
					pool.apply_async(download, args=(myargs,))
			else:
				filename = "%s.%s" % (var, filetails)
				filepath = "%s/%s.%s" % (dirname, var, filetails)
				url = "%s%s" % (url_heads, filepath)

				myargs = (filepath, url)
				pool.apply_async(download, args=(myargs,))

	pool.close()
	pool.join()