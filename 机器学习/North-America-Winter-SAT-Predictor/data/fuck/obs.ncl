load "$NCARG_ROOT/lib/ncarg/nclscripts/contrib/calendar_decode2.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"


year_start = 1979
year_end = 2018

tfile = addfile("CRU.nc","r")

tems = tfile->tmp
lat = tfile->lat
lon = tfile->lon
time = calendar_decode2(tfile->time,0)
year_idx=ind(time(:,0).ge.year_start.and.time(:,0).le.year_end)

ntime = year_end - year_start + 1

tem = tems(year_idx,:,:)

JAN = tem(2::12,:,:)
FEB = tem(3::12,:,:)
DEC= tem(4::12,:,:)

DJF = (DEC(0:ntime-1,:,:)+JAN(0:ntime-1,:,:)+FEB(0:ntime-1,:,:))/3.0
copy_VarMeta(DEC(0:ntime-1,:,:), DJF)

;ff = addfile("../NA-SAT-EOF/air.2m.mon.mean.nc","r")
;tt = short2flt(ff->air)
;tlat = ff->lat
;tlon = ff->lon

;djf = linint2_Wrap(lon,lat,DJF,True,tlon,tlat(::-1),0)

lat_idx = ind(lat.le.70.and.lat.ge.10)
lon_idx = ind(lon.ge.210.and.lon.le.320)

system("rm -rf obs.nc")
out = addfile("obs.nc","c")
out->tmp = DJF    ;(:,lat_idx,lon_idx)
