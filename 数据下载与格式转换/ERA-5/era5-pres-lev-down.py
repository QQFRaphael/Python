import os
import cdsapi

mons = ['01','02','03','04','05','06','07','08','09','10','11','12']
days = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
times = ['00:00','01:00','02:00','03:00','04:00','05:00','06:00','07:00','08:00','09:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00','18:00','19:00','20:00','21:00','22:00','23:00']
region = [62,68,8,142] # north, west, south, east
#levs = ['1', '2', '3', '5', '7', '10', '20', '30', '50', '70', '100', '125', '150', '175', '200', '225', '250', '300', '350', '400', '450', '500', '550', '600', '650', '700', '750', '775', '800', '825', '850', '875', '900', '925', '950', '975', '1000']
levs = ['200', '500', '750', '850', '925', '1000']


vars = ['relative_humidity'] #, 'specific_humidity', 'temperature', 'u_component_of_wind', 'v_component_of_wind', 'vertical_velocity']
#vars = ['relative_humidity', 'specific_humidity', 'temperature', 'u_component_of_wind', 'v_component_of_wind', 'vertical_velocity']


c = cdsapi.Client()

for var in vars:
	for year in range(1943,2024):
		for mon in mons:
			for day in days:
				for time in times:
						filepath = "%s/%s/%s/%s" % (var, year, mon, day)
						if not os.path.exists(filepath): os.makedirs(filepath)
						filename = "%s.nc" % time[0:2]
						try:
							c.retrieve(
								'reanalysis-era5-pressure-levels',
								{
									'product_type': 'reanalysis',
									'format': 'netcdf',
									'variable': var,
									'year': year,
									'month': mon,
									'day': day,
									'time': time,
									'area': region,
									'pressure_level': levs,
								},
								"%s/%s" % (filepath, filename)
								)
							print("%s/%s" % (filepath, filename))
							print("=====================================================================================")
						except:
							print("=====================================================================================")
							ff = open("era-missing-pres-lev.txt", "a+")
							ff.write("%s/%s\n" % (filepath, filename))
							continue

