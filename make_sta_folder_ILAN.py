import os
import shutil
import pandas as pd
import datetime

csv_url = './stalst_ILAN' #station list
df = pd.read_table(csv_url, delimiter= ' ', names=['sta', 'Lon','Lat','H(m)']) #name cloumn
sta_list=[]
sta_list=list(df['sta'])
datelist = os.listdir('./Sorted_oneday_ILAN_array')
datelist.sort()
datelist=datelist[183:214]

#FM.1032..DPE.20220629.SAC
#3001.FM.00.DPZ.2022.291.20221018.SAC

for date in datelist:
	datefolder = "./Sorted_oneday_ILAN_array/"+str(date)+"/"
	#print(datefolder) #./Sorted_oneday_ILAN_array/20230725/
	for sta in sta_list:
		#os.makedirs(datefolder+str(sta), exist_ok=True)
		#os.system('mv '+datefolder+str(sta)+'*.SAC.decon'+datefolder+str(sta)+'/')
		#print(datefolder+str(sta)) #./Sorted_oneday_ILAN_array/20230725/2028

		for ext in ['DPE', 'DPN', 'DPZ']:  # Assuming your files have these extensions
			day = date[4:8]
			fmt = '%m%d'
			dt=datetime.datetime.strptime(day,fmt)
			jdate=dt.timetuple()
			jdy=jdate.tm_yday
			file_name = f"{sta}.FM.00.{ext}.{date[0:4]}.{jdy}.{date}.SAC"  # Construct the file name
			source_file = f"{datefolder}{file_name}"  # Source file path
			dest_file = f"{date}/{sta}"  # Destination file path
			move_file=f"{datefolder}{str(sta)}"
			#print(file_name,dest_file)
			#print(source_file, move_file)
			if os.path.exists(source_file):  # Check if the file exists
				shutil.move(source_file, move_file)  # Move the file
