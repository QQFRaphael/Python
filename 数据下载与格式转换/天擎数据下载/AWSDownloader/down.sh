#!/bin/bash

source /public/software/profile.d/utils_anacoda2-env.sh
export TZ=UTC

starttime=$(date -d '5 minute ago' +%Y%m%d%H%M%S)
endtime=$(date +%Y%m%d%H%M%S)
echo ${starttime}
echo ${endtime}

## -------------------------------------------##

/bin/cat > /public/home/rmaps/data/zhejiang/Downloader/AWSDownloader/Skylar.in << EOF
nc
${starttime},${endtime}
/public/home/rmaps/data/zhejiang/raw/aws/aws5min_1x
26.84,117.44,31.40,123.36
Station_Name sname,Station_Id_C stid,Datetime obs_time,Lon lon,Lat lat,Alti elev,WIN_S_INST wsi,WIN_D_INST wdi,WIN_S_Gust_Max wsm,WIN_D_Gust_Max wdm,WIN_S_Avg_10mi ws10a,WIN_D_Avg_10mi wd10a,WIN_S_Avg_2mi ws2a,WIN_D_Avg_2mi wd2a,TEM taa,RHU rha,PRE pri,PRS paa
Station_Id_C stid,PRE_1h pr1,RHU_Min rhm,TEM_Max tax,TEM_Min tam,PRS_Max pax,PRS_Min pam,PRS_Max_OTime paxt,PRS_Min_OTime pamt,TEM_Max_OTime taxt,TEM_Min_OTime tamt,RHU_Min_OTIME rhmt,WIN_S_Inst_Max wsx,WIN_D_INST_Max wdx,WIN_S_INST_Max_OTime wsxt,WIN_S_Avg_10mi wsmt
EOF

/public/software/utils/anaconda2/bin/python /public/home/rmaps/data/zhejiang/Downloader/AWSDownloader/Skylar.py</public/home/rmaps/data/zhejiang/Downloader/AWSDownloader/Skylar.in


