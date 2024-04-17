import os
import glob
import datetime

data_data_ILAN = r"./Sorted_oneday_ILAN_array/"
allFileList = os.listdir(data_data_ILAN)
allFileList.sort()

for file in allFileList:
  try:
    if int(file) >= 20230101 and int(file) <= 20230131:
      data_sac = r"./Sorted_oneday_ILAN_array/"+file
      test=os.listdir(data_sac)
      print(test)
      for f in test:
          tt= os.path.split(f)[1]
          sta = tt.split('.')[0]
          fm = tt.split('.')[1]
          num = tt.split('.')[2]
          chan = tt.split('.')[3]
          year = tt.split('.')[4]
          date = tt.split('.')[7]
          day = tt.split('.')[7][4:8]
          fmt = '%m%d'
          dt=datetime.datetime.strptime(day,fmt)
          jdate=dt.timetuple()
          jdy=jdate.tm_yday
          print(jdy)
          print(data_sac+"/"+tt,data_sac+'/'+sta+"."+fm+".00."+chan+".2023."+str(jdy)+"."+date+".SAC")
  except:
        continue

#FM.3040..DPN.20220727.SAC (original)
#4021.FM.00.DPE.2022.jdy.20220727.SAC (change to)
