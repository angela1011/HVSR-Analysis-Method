import obspy
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram, convolve
from obspy import read, Trace, UTCDateTime
from scipy.io.wavfile import read
from scipy.fftpack import fft
import matplotlib.gridspec as gridspec
import math
import multiprocessing
import datetime
import os

def getFFT(data, log_scale=False):
    try:
        FFT = np.abs(np.fft.rfft(data)[1:])
    except:
        FFT = np.fft.fft(data)
        left, right = np.split(np.abs(FFT), 2)
        FFT = np.add(left, right[::-1])

    if log_scale:
        try:
            FFT = np.multiply(20, np.log10(FFT))
        except Exception as e:
            print('Log(FFT) failed: %s' %str(e))
    return FFT
def getFreq(data_size,dt):
    fftx = np.fft.fftfreq(data_size, dt)
    fftx = np.split(np.abs(fftx), 2)[0][1:]
    return fftx

date_list=["20220831","20220901","20220902","20220903"]
for i in range(len(date_list)):
    date=date_list[i]
    fmt = '%Y%m%d'
    d=datetime.datetime.strptime(date,fmt)
    jdate=d.timetuple()
    jdy=jdate.tm_yday

    sta_list=[] 
    lon_list=[] 
    lat_list=[]
    f=open("./stalst_ILAN").readlines()[:]
    for i in range(len(f)):
        sta_list.append(f[i].split(" ")[0])
        lon_list.append(f[i].split(" ")[1])
        lat_list.append(f[i].split(" ")[2])
        sta_list=sorted(sta_list)
    for s in range(len(sta_list)):
        sta=sta_list[s]
        lon=lon_list[s]
        lat=lat_list[s]

        try:
    ##input file
            file_E ="./Sorted_oneday_ILAN_array/"+date+"/"+ sta +"/"+ sta +".FM.00.DPE.2022."+str(jdy)+"."+date+".SAC"
            file_N ="./Sorted_oneday_ILAN_array/"+date+"/"+ sta +"/"+ sta +".FM.00.DPN.2022."+str(jdy)+"."+date+".SAC"
            file_Z ="./Sorted_oneday_ILAN_array/"+date+"/"+ sta +"/"+ sta +".FM.00.DPZ.2022."+str(jdy)+"."+date+".SAC"
    
    ##obspy read file
            st_E=obspy.read(file_E) 
            st_N=obspy.read(file_N)
            st_Z=obspy.read(file_Z)
        except:
            continue

        data_E = st_E[0].data
        dt = 1/(st_E[0].stats.sampling_rate)


        dt_E = st_E[0].stats.starttime
        dt_N = st_N[0].stats.starttime
        dt_Z = st_Z[0].stats.starttime

        # st_E_1=st_E.copy()
        # st_N_1=st_N.copy()  
        # st_Z_1=st_Z.copy()
        # st_E_1.trim(dt_E,dt_E+3600.0) #0-20s
        # st_N_1.trim(dt_E,dt_E+3600.0)
        # st_Z_1.trim(dt_E,dt_E+3600.0)

        #dt_ENZ=dt_E+57600 ##16hr
        #dt_ENZ=dt_E+21600 ##6hr
        #dt_ENZ=dt_E+57600  ##16hr #0-1hr 
        #dt_ENZ=dt_E+61200  ##17hr #1-2hr
        #dt_ENZ=dt_E+64800  ##18hr #2-3hr
        #dt_ENZ=dt_E+68400  ##19hr #3-4hr
        dt_ENZ=dt_E+72000  ##20hr #4-5hr
        
        st_E_1=st_E.copy()
        st_N_1=st_N.copy()  
        st_Z_1=st_Z.copy()
        st_E_1.trim(dt_ENZ,dt_ENZ+3600.0) #0-20s
        st_N_1.trim(dt_ENZ,dt_ENZ+3600.0)
        st_Z_1.trim(dt_ENZ,dt_ENZ+3600.0)

        test=[]
        ##32-45mins->20s ##16-30min->30s and 30mins->60s
        for i in range(1,180):  #20s(1Hz) in 1hr=60*3=180
            st2_E=st_E.copy()
            st2_N=st_N.copy()  
            st2_Z=st_Z.copy()
            # st2_E.trim(dt_E,dt_E+20.0) #0-20s
            # st2_N.trim(dt_E,dt_E+20.0)
            # st2_Z.trim(dt_E,dt_E+20.0)
            # dt_E=dt_E+20.0
            st2_E.trim(dt_ENZ,dt_ENZ+20.0) #0-20s
            st2_N.trim(dt_ENZ,dt_ENZ+20.0)
            st2_Z.trim(dt_ENZ,dt_ENZ+20.0)
            dt_ENZ=dt_ENZ+20.0

            data_E = st2_E[0].data
            data_N = st2_N[0].data
            data_Z = st2_Z[0].data

            testdata_E=getFFT(data_E,log_scale=False)
            testfreq_E=getFreq((len(testdata_E)+1)*2,dt)
            testdata_N=getFFT(data_N,log_scale=False)
            testfreq_N=getFreq((len(testdata_N)+1)*2,dt)
            testdata_Z=getFFT(data_Z,log_scale=False)
            testfreq_Z=getFreq((len(testdata_Z)+1)*2,dt)
            
            HV= ((testdata_E)**2+(testdata_N)**2)**(1/2)/testdata_Z
            HV=HV[3:]
            test.append(HV)

        testfreq_Z=testfreq_Z[3:]

        testmean=[]
        teststd=[]
        last_mean=[]
        last_mean2=[]
        pos=[]
        neg=[]
        pos_std=[]
        neg_std=[]
        last_std=[] 
        std_all=[] 

        for k in range(len(test[0])):
            for i in range(len(test)):
                testmean.append(test[i][k])
            mean_all = np.mean(testmean)
            testmean=[]
            last_mean.append(mean_all)

        testfreq_Z2=[]
        perc = 0.1
        for j in range(len(testfreq_Z)):  ##2/9-1250/11 1,2269
            if testfreq_Z[j] >= 0.2*(1+perc) and testfreq_Z[j] <= 15*(1-perc):
                testfreq_Z2.append(testfreq_Z[j])
                freq1=testfreq_Z[j]-testfreq_Z[j]*perc
                freq2=testfreq_Z[j]+testfreq_Z[j]*perc
                freqm=[]
                for i in range(len(testfreq_Z)):
                    if testfreq_Z[i] > freq1 and testfreq_Z[i] < freq2:
                        freqm.append(last_mean[i])
                last_mean2.append(np.mean(freqm))

        max_index = last_mean2.index(max(last_mean2))

        shift_distance_x = 0.65
        shift_distance_y = 1.0
        shift_distance = 2.0
        ##f0=VS/4h
        ##H=45.7f**-1.26
        Vs=(1.58597+2.17865)/2
        #121.7 24.7 0.47299 1.58597 0.0411815
        #121.7 24.7 0.97299 2.17865 0.0282429
        ##Depth = 45.7*(testfreq_Z2[max_index]**(-1.26))
        ##Depth_M = 30.8*(testfreq_Z2[max_index]**(-1.39))
        HCL_depth = Vs/(testfreq_Z2[max_index]*4)

        path = 'ori_am_4_5_Ilan_'+date+'.txt'
        with open(path, 'a') as f:
            print(sta, lon, lat, testfreq_Z2[max_index], last_mean2[max_index], HCL_depth, file=f)
        
        os.makedirs("./ILAN_depth/ori_AM_4_5_"+date, exist_ok=True)    
        path="./ILAN_depth/ori_AM_4_5_"+date+"/"+sta+"_HV.txt"
        with open(path, 'a') as f:  
            for i in range(len(testfreq_Z2)):
                print(testfreq_Z2,last_mean2,file=f)

        #with open(path, 'a') as f:
        #    print(sta,lon,lat,testfreq_Z2[max_index],last_mean2[max_index],HCL_depth, file=f)

        #plot fig
        gs=gridspec.GridSpec(4, 2, height_ratios=[0.5, 0.5, 0.5, 1])
        ax1 = plt.subplot(gs[0, :])
        ax2 = plt.subplot(gs[1, :])
        ax3 = plt.subplot(gs[2, :])
        ax4 = plt.subplot(gs[3, 0])
        ax5 = plt.subplot(gs[3, 1])

        ax1.set_title(f'{sta}_{date}\nE')
        ax1.plot(st_E_1[0].times("matplotlib"),st_E_1[0].data,label='E',color='cornflowerblue',linewidth=0.5)
        ax1.xaxis_date() 
        ax2.set_title('N')
        ax2.plot(st_N_1[0].times("matplotlib"),st_N_1[0].data,label='N',color='tomato',linewidth=0.5)
        ax2.xaxis_date() 
        ax3.set_title('Z')
        ax3.plot(st_Z_1[0].times("matplotlib"),st_Z_1[0].data,label='Z',color='mediumseagreen',linewidth=0.5)
        ax3.xaxis_date() 
        ax4.set_title('FFT')
        mask = (testfreq_E >= 0.2) & (testfreq_E <= 15)
        maskn = (testfreq_N >= 0.2) & (testfreq_N <= 15)
        maskz = (testfreq_Z >= 0.2) & (testfreq_Z <= 15)
        ax4.plot(testfreq_E[mask], testdata_E[mask],label='E',color='cornflowerblue',linewidth=0.5)
        ax4.plot(testfreq_N[maskn], testdata_N[maskn], label='N', color='tomato', linewidth=0.5)
        ax4.plot(testfreq_Z2, testdata_Z[3:269],label='Z',color='mediumseagreen',linewidth=0.5)
        ax5.set_xlim([0.2, 15])
        ax4.set_xscale('log')
        ax4.set_yscale('log')
        ax4.set_xlabel("Frequency(Hz)", fontsize = 8)
        
        ax5.set_title('H/V')
        ax5.plot(testfreq_Z,last_mean,label='Mean',color='cornflowerblue',zorder=1)
        ax5.plot(testfreq_Z2,last_mean2,label='Average smooth',color='tomato',zorder=2) 
        ax5.scatter(testfreq_Z2[max_index],last_mean2[max_index],color='red',s=10,label='Max Value',zorder=3)
        ax5.text(testfreq_Z2[max_index] * shift_distance_x ,last_mean2[max_index] + shift_distance_y,testfreq_Z2[max_index],fontsize=8,zorder=4)
        ax5.text(testfreq_Z2[max_index] * shift_distance_x ,last_mean2[max_index] - shift_distance_y,HCL_depth,fontsize=8,zorder=5)
        ax5.set_xlabel("Frequency(Hz)", fontsize = 8)
        ax5.set_xlim([0.2, 15])   #>5sec
        ax5.set_xscale('log') 
        ax5.set_ylim([0, max(last_mean2)*1.2]) 

        plt.tight_layout()
        os.makedirs("./ILAN_depth/ori_AM_4_5_"+date, exist_ok=True)
        plt.savefig("./ILAN_depth/ori_AM_4_5_"+date+"/"+sta+"_HV.png")
        plt.close()
