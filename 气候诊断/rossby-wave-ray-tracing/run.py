import os
import numpy as np

mylat = []
mylon = []
for yy in np.arange(65,75,2.5):
    for xx in np.arange(180,235,2.5):
        mylat.append(yy)
        mylon.append(xx)
mywavenumber = [1,2,3,4,5,6,7]

lat = np.linspace(90,-90,73)
lon = np.linspace(0,357.5,144)

os.system("./clean.sh")

for k in mywavenumber:
	for loc in zip(mylat, mylon):
		frcLat = loc[0]
		frcLon = loc[1]

		frcx = np.where(lon==frcLon)[0][0]
		frcy = np.where(lat==frcLat)[0][0]

		print("lat idx: %s    lon idx: %s" % (frcx, frcy))

		os.system("sed -i \"70s/^.*.*$/frcx=[%d];/g\" calc_2d_raytrace.m" % frcx)
		os.system("sed -i \"71s/^.*.*$/frcy=[%d];/g\" calc_2d_raytrace.m" % frcy)
		os.system("sed -i \"83s/^.*.*$/k_wavenumbers=[%d];/g\" calc_2d_raytrace.m" % k)

		os.system("matlab -nodesktop -nosplash -nodisplay -r \"run('calc_2d_raytrace.m');exit;\"")
