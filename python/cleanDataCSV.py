import pandas as pd
import matplotlib.pyplot as plt
import EMGfunctions as emgf

#if we need to merge files we import next line
#import EMGfunctions as emgf

column_names = [
    'emg',
    't',
]

#data = pd.read_csv('test_data.csv',sep=',', engine='python', names=column_names, skiprows=5,skipfooter=5)
data = pd.read_csv('test_data.csv',sep=',', engine='python', names=column_names)

plt.figure()
plt.plot(data.t, data.emg)
emg = data.emg
time = data.t

emgcorrectmean = emgf.remove_mean(emg,time)
emg_filtered = emgf.emg_filter(emgcorrectmean, time)
emg_rectified = emgf.emg_rectify(emg_filtered, time)

emg_filtered, emg_envelope = emgf.alltogether(time, emg, low_pass=2, sfreq=1000, high_band=20, low_band=450)