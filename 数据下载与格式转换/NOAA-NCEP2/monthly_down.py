import os
import time
import requests
import multiprocessing

# long term means are not downloaded in this script
# there are three kinds of data according to NOAA website: 
# surface, pressure, gaussian_grid

filetails = ".mon.mean.nc"

dirnames = ['surface', 'pressure', 'gaussian_grid']
surface = ['mslp', 'pres.sfc', 'pr_wtr.eatm']
pressure = ['air', 'hgt', 'omega', 'rhum', 'uwnd', 'vwnd', 'wspd']
gaussian_grid = ["air.2m", "cprat.sfc", "dlwrf.sfc", "dswrf.ntat", "dswrf.sfc", "gflux.sfc", "icec.sfc", "lhtfl.sfc", "pevpr.sfc", "prate.sfc", "pres.hcb", "pres.hct", "pres.lcb", "pres.lct", "pres.mcb", "pres.mct", "pres.sfc", "runof.sfc", "shtfl.sfc", "shum.2m", "skt.sfc", "soilw.0-10cm", "soilw.10-200cm", "tcdc.eatm", "tmax.2m", "tmin.2m", "tmp.0-10cm", "tmp.10-200cm", "uflx.sfc", "ugwd.sfc", "ulwrf.ntat", "ulwrf.sfc", "uswrf.ntat", "uswrf.sfc", "uwnd.10m", "vflx.sfc", "vgwd.sfc", "vwnd.10m", "weasd.sfc", "wspd.10m"]

url_heads = "https://downloads.psl.noaa.gov/Datasets/ncep.reanalysis2/Monthlies/"

def download(args):
	dirname = args[0]
	var = args[1]
	filetails = args[2]
	url_heads = args[3]

	url = "%s%s/%s%s" % (url_heads, dirname, var, filetails)

	filepath = "%s/%s%s" % (dirname, var, filetails)

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
	for dirname in dirnames:
		if not os.path.exists(dirname): os.makedirs(dirname)

	pool = multiprocessing.Pool(processes=4)

	for var in surface:
		myargs = ('surface', var, filetails, url_heads)
		pool.apply_async(download, args=(myargs,))

	for var in pressure:
		myargs = ('pressure', var, filetails, url_heads)
		pool.apply_async(download, args=(myargs,))

	for var in gaussian_grid:
		myargs = ('gaussian_grid', var, filetails, url_heads)
		pool.apply_async(download, args=(myargs,))

	pool.close()
	pool.join()