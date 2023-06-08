#!/bin/sh

for scene in ME ML neural SE SL VSE WE WL
do
	for bio in bio_01 bio_02 bio_03 bio_04 bio_05 bio_06 bio_07 bio_08 bio_09 bio_10 bio_11 bio_12 bio_13 bio_14 bio_15 bio_16 bio_17 bio_18 bio_19
	do
		gdal_translate $scene/$bio/sta.adf ../cru_china/$scene/${bio}.asc
		echo "================$scene   $bio================"
	done
done
