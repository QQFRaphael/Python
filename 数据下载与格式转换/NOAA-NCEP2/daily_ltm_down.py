import os
import time
import requests
import multiprocessing

# this script download the long term mean
# and daily long term mean

monfiletails = [".mon.ltm.nc", ".mon.ltm.1981-2010.nc", ".mon.ltm.1991-2020.nc"] 
dayfiletails = [".day.ltm.1981-2010.nc"]

surface = ['mslp', 'pr_wtr.eatm']
pressure = ['air', 'hgt', 'omega', 'rhum', 'uwnd', 'vwnd']
gaussian_grid = ["air.2m", "icec.sfc", "lhtfl.sfc", "prate.sfc", "skt.sfc", "ulwrf.ntat", "uwnd.10m", "vwnd.10m", "weasd.sfc"]

dailies_surface = ['mslp', 'pres', 'pr_wtr']
dailies_pressure = ['air', 'hgt', 'omega', 'rhum', 'uwnd', 'vwnd']
dailies_gauss = ['prate.sfc.gauss', 'skt.sfc.gauss']

dirs = {
	"LTMs/Dailies/surface/": dailies_surface,
	"LTMs/Dailies/pressure/": dailies_pressure,
	"LTMs/Dailies/gaussian_grid/": dailies_gauss,
	"LTMs/gaussian_grid/": gaussian_grid,
	"LTMs/pressure/": pressure,
	"LTMs/surface/": surface
}

url_heads = "https://downloads.psl.noaa.gov/Datasets/ncep.reanalysis2/Monthlies/"

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
	pool = multiprocessing.Pool(processes=4)

	for dirname in dirs.keys():
		if dirname in ("LTMs/Dailies/surface/", "LTMs/Dailies/pressure/", "LTMs/Dailies/gaussian_grid/"):
			filetails = dayfiletails
		else:
			filetails= monfiletails
	
		if not os.path.exists(dirname): os.makedirs(dirname)
	
		for var in dirs[dirname]:
			for tail in filetails:
				filepath = "%s%s%s" % (dirname, var, tail)
				url = "%s%s" % (url_heads, filepath)
	
				myargs = (filepath, url)
				pool.apply_async(download, args=(myargs,))
	pool.close()
	pool.join()