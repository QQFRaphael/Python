import numpy as np
import xarray as xr
from obtain_coords_dict import obtain_coords_dict

def TwoMonth(var, season, operate, year_start, year_end):
	"""
	year_end may be confusing. Take 2019 as an example, JFM of 2019 is 2019.01-03
	while DJF of 2019 is 2019.12-2020.02
	"""
	var_jan = var.sel(time=var.time.dt.month.isin(1)&var.time.dt.year.isin([x for x in range(year_start,year_end)])) 
	var_feb = var.sel(time=var.time.dt.month.isin(2)&var.time.dt.year.isin([x for x in range(year_start,year_end)])) 
	var_mar = var.sel(time=var.time.dt.month.isin(3)&var.time.dt.year.isin([x for x in range(year_start,year_end)])) 
	var_apr = var.sel(time=var.time.dt.month.isin(4)&var.time.dt.year.isin([x for x in range(year_start,year_end)])) 
	var_may = var.sel(time=var.time.dt.month.isin(5)&var.time.dt.year.isin([x for x in range(year_start,year_end)])) 
	var_jun = var.sel(time=var.time.dt.month.isin(6)&var.time.dt.year.isin([x for x in range(year_start,year_end)])) 
	var_jul = var.sel(time=var.time.dt.month.isin(7)&var.time.dt.year.isin([x for x in range(year_start,year_end)])) 
	var_aug = var.sel(time=var.time.dt.month.isin(8)&var.time.dt.year.isin([x for x in range(year_start,year_end)])) 
	var_sep = var.sel(time=var.time.dt.month.isin(9)&var.time.dt.year.isin([x for x in range(year_start,year_end)])) 
	var_oct = var.sel(time=var.time.dt.month.isin(10)&var.time.dt.year.isin([x for x in range(year_start,year_end)])) 
	var_nov = var.sel(time=var.time.dt.month.isin(11)&var.time.dt.year.isin([x for x in range(year_start,year_end)])) 
	var_dec = var.sel(time=var.time.dt.month.isin(12)&var.time.dt.year.isin([x for x in range(year_start,year_end)])) 
	var_jan_next = var.sel(time=var.time.dt.month.isin(1)&var.time.dt.year.isin([x for x in range(year_start+1,year_end+1)])) 
	var_feb_next = var.sel(time=var.time.dt.month.isin(2)&var.time.dt.year.isin([x for x in range(year_start+1,year_end+1)])) 

	if operate == "add":
		div_factor = 1.0
	elif operate ==  "ave":
		div_factor = 2.0

	if season == "JF":
		month_idx = [1, 2]
	elif season == "FM":
		month_idx = [2, 3]
	elif season == "MA":
		month_idx = [3, 4]
	elif season == "AM":
		month_idx = [4, 5]
	elif season == "MJ":
		month_idx = [5, 6]
	elif season == "JJ":
		month_idx = [6, 7]
	elif season == "JA":
		month_idx = [7, 8]
	elif season == "AS":
		month_idx = [8, 9]
	elif season == "SO":
		month_idx = [9, 10]
	elif season == "ON":
		month_idx = [10, 11]
	elif season == "ND":
		month_idx = [11, 12]
	elif season == "DJ":
		month_idx = [12, 1]


	if season == "DJ":
		var1 = var.sel(time=var.time.dt.month.isin(month_idx[0])&var.time.dt.year.isin([x for x in range(year_start,year_end)])) 
		var2 = var.sel(time=var.time.dt.month.isin(month_idx[1])&var.time.dt.year.isin([x for x in range(year_start+1,year_end+1)])) 
	else:
		var1 = var.sel(time=var.time.dt.month.isin(month_idx[0])&var.time.dt.year.isin([x for x in range(year_start,year_end)])) 
		var2 = var.sel(time=var.time.dt.month.isin(month_idx[1])&var.time.dt.year.isin([x for x in range(year_start,year_end)])) 

	tmp = (var1.values + var2.values) / div_factor

	coords = obtain_coords_dict(var1)

	var_season = xr.DataArray(tmp, coords=coords)
	
	return var_season
