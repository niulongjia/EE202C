# Scientific libraries
# import plotly.plotly as py
# import plotly.graph_objs as go
import numpy as np
from numpy import genfromtxt
import os
import os.path
import random
import sys
import numpy.fft as fft
import heapq
import time
from numpy import mean, sqrt, square, arange



#index of cvs files ---->NEEDS TO BE CHANGED 
TIME  = 0
ACC_X = 3
ACC_Y = 4
ACC_Z = 5
GYRO_X = 6
GYRO_Y = 7
GYRO_Z = 8

train_data_ELBOW = []
train_data_RIGHT_Wrist = []
train_data_LEFT_Wrist = []


features = []
my_ACC_X_coe = []
my_ACC_Y_coe = []
my_ACC_Z_coe = []
my_GYRO_X_coe = []
my_GYRO_Y_coe = []
my_GYRO_Z_coe = []
ACC_X_data = [] 
ACC_Y_data = [] 
ACC_Z_data = [] 
GYRO_X_data = [] 
GYRO_Y_data = [] 
GYRO_Z_data = [] 
numfiles = 0
preNumFiles = 0
pre_number = 0
number = 0
# trainfile = open('coefficient_data_train.txt','w')
while 1:
	filelist =  sorted([f for f in os.listdir('.') if f.lower().endswith('.csv')],key = os.path.getctime,reverse = True)
	numfiles = len(filelist)
	mostupdated = max([f for f in os.listdir('.') if f.lower().endswith('.csv')],key = os.path.getctime)
	filewithoutext=mostupdated.split('.')[0]
	number = filewithoutext.split('_')[4]
	if number == pre_number:
		continue
	pre_number = number
	filelist = []
	if number == 0:
		number =1 
	filelist.append("NINEDOF_1_RIGHT_WRIST_" + str(int(number)-1)+ ".csv")
	filelist.append("NINEDOF_2_RIGHT_ELBOW_" + str(int(number)-1)+ ".csv")
	filelist.append("NINEDOF_3_LEFT_WRIST_" + str(int(number)-1)+ ".csv")
	print filelist 
	# if numfiles - preNumFiles < 3:
	# 	print 'next while \n'
	# 	continue
	# preNumFiles = numfiles
	# print filelist
	# filelist = filelist[3:6]

	# print filelist

	train_data_ELBOW = []
	train_data_RIGHT_Wrist = []
	train_data_LEFT_Wrist = []

	if "RIGHT_WRIST" and "RIGHT_ELBOW" and "LEFT_WRIST" in ' '.join(filelist):
		for filename in filelist:
			if 'RIGHT_WRIST' in filename:
				train_data_RIGHT_Wrist.append(genfromtxt(filename, delimiter=','))
			elif 'LEFT_WRIST' in filename:
				train_data_LEFT_Wrist.append(genfromtxt(filename, delimiter=','))
			elif 'ELBOW' in filename:
				train_data_ELBOW.append(genfromtxt(filename, delimiter=','))
	    
		for (data, data_2 ,data_3)in zip(train_data_RIGHT_Wrist, train_data_LEFT_Wrist, train_data_ELBOW):

			# ACC_data_rms = np.array(np.sqrt(np.array(np.array(data[1:,ACC_X])**2+np.array(data[1:,ACC_Y])**2+np.array(data[1:,ACC_Z])**2)))
			# GYRO_data_rms = np.array(np.sqrt(np.array(np.array(data[1:,GYRO_X])**2+np.array(data[1:,GYRO_Y])**2+np.array(data[1:,GYRO_Z])**2)))
			# ACC_data2_rms = np.array(np.sqrt(np.array(np.array(data_2[1:,ACC_X])**2+np.array(data_2[1:,ACC_Y])**2+np.array(data_2[1:,ACC_Z])**2)))
			# GYRO_data2_rms = np.array(np.sqrt(np.array(np.array(data_2[1:,GYRO_X])**2+np.array(data_2[1:,GYRO_Y])**2+np.array(data_2[1:,GYRO_Z])**2)))
			

			line = ''
			#data[1:,0] = data[1:,0]-data[1,0]
			my_ACC_coe = []
			my_GYRO_coe = []

			ACC_peak_percent = 0;
			GYRO_peak_percent = 0;



			ACC_X_data = np.absolute(data[1:,ACC_X])
			ACC_Y_data = np.absolute(data[1:,ACC_Y])
			ACC_Z_data = np.absolute(data[1:,ACC_Z]) 
			GYRO_X_data = np.absolute(data[1:,GYRO_X])
			GYRO_Y_data = np.absolute(data[1:,GYRO_Y])
			GYRO_Z_data = np.absolute(data[1:,GYRO_Z])

			#ACC_X
			ACC_mean = np.mean(ACC_X_data)/3
			ACC_std = np.std(ACC_X_data, ddof=1)/3
			ACC_peak = (max(ACC_X_data) - min(ACC_X_data))/5
			ACC_peak_rms = (sqrt(mean(square(ACC_X_data))))/3

			ACC_peak_percent = 0
			for entry in ACC_X_data:
				if entry >= abs(ACC_mean*1.25):
					ACC_peak_percent += 1

			my_ACC_coe.append(str(ACC_mean))
			my_ACC_coe.append(str(ACC_std))
			my_ACC_coe.append(str(ACC_peak))
			my_ACC_coe.append(str(ACC_peak_rms))
			my_ACC_coe.append(str(ACC_peak_percent/len(ACC_X_data)))

			#ACC_Y
			ACC_mean = np.mean(ACC_Y_data)/3
			ACC_std = np.std(ACC_Y_data, ddof=1)/3
			ACC_peak = (max(ACC_Y_data) - min(ACC_Y_data))/5
			ACC_peak_rms = sqrt(mean(square(ACC_Y_data)))/3
			ACC_peak_percent = 0
			for entry in ACC_Y_data:
				if entry >= abs(ACC_mean*1.25):
					ACC_peak_percent += 1

			my_ACC_coe.append(str(ACC_mean))
			my_ACC_coe.append(str(ACC_std))
			my_ACC_coe.append(str(ACC_peak))
			my_ACC_coe.append(str(ACC_peak_rms))
			my_ACC_coe.append(str(ACC_peak_percent/len(ACC_Y_data)))

			#ACC_Z
			ACC_mean = np.mean(ACC_Z_data)/3
			ACC_std = np.std(ACC_Z_data, ddof=1)/3
			ACC_peak = (max(ACC_Z_data) - min(ACC_Z_data))/5
			ACC_peak_rms = sqrt(mean(square(ACC_Z_data)))/3
			ACC_peak_percent = 0
			for entry in ACC_Z_data:
				if entry >= abs(ACC_mean*1.25):
					ACC_peak_percent += 1

			my_ACC_coe.append(str(ACC_mean))
			my_ACC_coe.append(str(ACC_std))
			my_ACC_coe.append(str(ACC_peak))
			my_ACC_coe.append(str(ACC_peak_rms))
			my_ACC_coe.append(str(ACC_peak_percent/len(ACC_Z_data)))

			#GYRO_X 
			GYRO_mean = np.mean(GYRO_X_data)/100
			GYRO_std = np.std(GYRO_X_data, ddof=1)/100
			GYRO_peak = (max(GYRO_X_data) - min(GYRO_X_data) )/200
			GYRO_peak_rms = sqrt(mean(square(GYRO_X_data)))/150
			GYRO_peak_percent= 0
			for entry in GYRO_X_data:
				if entry >= abs(GYRO_mean*1.25):
					GYRO_peak_percent += 1

			my_GYRO_coe.append(str(GYRO_mean))
			my_GYRO_coe.append(str(GYRO_std))
			my_GYRO_coe.append(str(GYRO_peak))
			my_GYRO_coe.append(str(GYRO_peak_rms))
			my_GYRO_coe.append(str(GYRO_peak_percent/len(GYRO_X_data)))

			#GYRO_Y
			GYRO_mean = np.mean(GYRO_Y_data)/100
			GYRO_std = np.std(GYRO_Y_data, ddof=1)/100
			GYRO_peak = (max(GYRO_Y_data) - min(GYRO_Y_data) )/200
			GYRO_peak_rms = sqrt(mean(square(GYRO_Y_data)))/150
			GYRO_peak_percent =0
			for entry in GYRO_Y_data:
				if entry >= abs(GYRO_mean*1.25):
					GYRO_peak_percent += 1
			my_GYRO_coe.append(str(GYRO_mean))
			my_GYRO_coe.append(str(GYRO_std))
			my_GYRO_coe.append(str(GYRO_peak))
			my_GYRO_coe.append(str(GYRO_peak_rms))
			my_GYRO_coe.append(str(GYRO_peak_percent/len(GYRO_Y_data)))

			#GYRO_Z
			GYRO_mean = np.mean(GYRO_Z_data)/100
			GYRO_std = np.std(GYRO_Z_data, ddof=1)/100
			GYRO_peak =(max(GYRO_Z_data) - min(GYRO_Z_data)) /200
			GYRO_peak_rms = sqrt(mean(square(GYRO_Z_data)))/150
			GYRO_peak_percent = 0
			for entry in GYRO_Z_data:
				if entry >= abs(GYRO_mean*1.25):
					GYRO_peak_percent += 1
			my_GYRO_coe.append(str(GYRO_mean))
			my_GYRO_coe.append(str(GYRO_std))
			my_GYRO_coe.append(str(GYRO_peak))
			my_GYRO_coe.append(str(GYRO_peak_rms))
			my_GYRO_coe.append(str(GYRO_peak_percent/len(GYRO_Z_data)))


			ACC_X_data = np.absolute(data_2[1:,ACC_X])
			ACC_Y_data = np.absolute(data_2[1:,ACC_Y])
			ACC_Z_data = np.absolute(data_2[1:,ACC_Z])
			GYRO_X_data = np.absolute(data_2[1:,GYRO_X])
			GYRO_Y_data = np.absolute(data_2[1:,GYRO_Y])
			GYRO_Z_data = np.absolute(data_2[1:,GYRO_Z])

			#ACC_X
			ACC_mean = np.mean(ACC_X_data)/3
			ACC_std = np.std(ACC_X_data, ddof=1)/3
			ACC_peak = (max(ACC_X_data) - min(ACC_X_data))/5
			ACC_peak_rms = (sqrt(mean(square(ACC_X_data))))/3

			ACC_peak_percent = 0
			for entry in ACC_X_data:
				if entry >= abs(ACC_mean*1.25):
					ACC_peak_percent += 1

			my_ACC_coe.append(str(ACC_mean))
			my_ACC_coe.append(str(ACC_std))
			my_ACC_coe.append(str(ACC_peak))
			my_ACC_coe.append(str(ACC_peak_rms))
			my_ACC_coe.append(str(ACC_peak_percent/len(ACC_X_data)))

			#ACC_Y
			ACC_mean = np.mean(ACC_Y_data)/3
			ACC_std = np.std(ACC_Y_data, ddof=1)/3
			ACC_peak = (max(ACC_Y_data) - min(ACC_Y_data))/5
			ACC_peak_rms = sqrt(mean(square(ACC_Y_data)))/3
			ACC_peak_percent = 0
			for entry in ACC_Y_data:
				if entry >= abs(ACC_mean*1.25):
					ACC_peak_percent += 1

			my_ACC_coe.append(str(ACC_mean))
			my_ACC_coe.append(str(ACC_std))
			my_ACC_coe.append(str(ACC_peak))
			my_ACC_coe.append(str(ACC_peak_rms))
			my_ACC_coe.append(str(ACC_peak_percent/len(ACC_Y_data)))

			#ACC_Z
			ACC_mean = np.mean(ACC_Z_data)/3
			ACC_std = np.std(ACC_Z_data, ddof=1)/3
			ACC_peak = (max(ACC_Z_data) - min(ACC_Z_data))/5
			ACC_peak_rms = sqrt(mean(square(ACC_Z_data)))/3
			ACC_peak_percent = 0
			for entry in ACC_Z_data:
				if entry >= abs(ACC_mean*1.25):
					ACC_peak_percent += 1

			my_ACC_coe.append(str(ACC_mean))
			my_ACC_coe.append(str(ACC_std))
			my_ACC_coe.append(str(ACC_peak))
			my_ACC_coe.append(str(ACC_peak_rms))
			my_ACC_coe.append(str(ACC_peak_percent/len(ACC_Z_data)))

			#GYRO_X 
			GYRO_mean = np.mean(GYRO_X_data)/100
			GYRO_std = np.std(GYRO_X_data, ddof=1)/100
			GYRO_peak = (max(GYRO_X_data) - min(GYRO_X_data) )/200
			GYRO_peak_rms = sqrt(mean(square(GYRO_X_data)))/150
			GYRO_peak_percent= 0
			for entry in GYRO_X_data:
				if entry >= abs(GYRO_mean*1.25):
					GYRO_peak_percent += 1

			my_GYRO_coe.append(str(GYRO_mean))
			my_GYRO_coe.append(str(GYRO_std))
			my_GYRO_coe.append(str(GYRO_peak))
			my_GYRO_coe.append(str(GYRO_peak_rms))
			my_GYRO_coe.append(str(GYRO_peak_percent/len(GYRO_X_data)))

			#GYRO_Y
			GYRO_mean = np.mean(GYRO_Y_data)/100
			GYRO_std = np.std(GYRO_Y_data, ddof=1)/100
			GYRO_peak = (max(GYRO_Y_data) - min(GYRO_Y_data) )/200
			GYRO_peak_rms = sqrt(mean(square(GYRO_Y_data)))/150
			GYRO_peak_percent =0
			for entry in GYRO_Y_data:
				if entry >= abs(GYRO_mean*1.25):
					GYRO_peak_percent += 1
			my_GYRO_coe.append(str(GYRO_mean))
			my_GYRO_coe.append(str(GYRO_std))
			my_GYRO_coe.append(str(GYRO_peak))
			my_GYRO_coe.append(str(GYRO_peak_rms))
			my_GYRO_coe.append(str(GYRO_peak_percent/len(GYRO_Y_data)))

			#GYRO_Z
			GYRO_mean = np.mean(GYRO_Z_data)/100
			GYRO_std = np.std(GYRO_Z_data, ddof=1)/100
			GYRO_peak = (max(GYRO_Z_data) - min(GYRO_Z_data) )/200
			GYRO_peak_rms = sqrt(mean(square(GYRO_Z_data)))/150
			GYRO_peak_percent = 0
			for entry in GYRO_Z_data:
				if entry >= abs(GYRO_mean*1.25):
					GYRO_peak_percent += 1
			my_GYRO_coe.append(str(GYRO_mean))
			my_GYRO_coe.append(str(GYRO_std))
			my_GYRO_coe.append(str(GYRO_peak))
			my_GYRO_coe.append(str(GYRO_peak_rms))
			my_GYRO_coe.append(str(GYRO_peak_percent/len(GYRO_Z_data)))


			ACC_X_data = np.absolute(data_3[1:,ACC_X])
			ACC_Y_data = np.absolute(data_3[1:,ACC_Y])
			ACC_Z_data = np.absolute(data_3[1:,ACC_Z])
			GYRO_X_data = np.absolute(data_3[1:,GYRO_X])
			GYRO_Y_data = np.absolute(data_3[1:,GYRO_Y])
			GYRO_Z_data = np.absolute(data_3[1:,GYRO_Z])

			#ACC_X
			ACC_mean = np.mean(ACC_X_data)/3
			ACC_std = np.std(ACC_X_data, ddof=1)/3
			ACC_peak = (max(ACC_X_data) - min(ACC_X_data))/5
			ACC_peak_rms = (sqrt(mean(square(ACC_X_data))))/3

			ACC_peak_percent = 0
			for entry in ACC_X_data:
				if entry >= abs(ACC_mean*1.25):
					ACC_peak_percent += 1

			my_ACC_coe.append(str(ACC_mean))
			my_ACC_coe.append(str(ACC_std))
			my_ACC_coe.append(str(ACC_peak))
			my_ACC_coe.append(str(ACC_peak_rms))
			my_ACC_coe.append(str(ACC_peak_percent/len(ACC_X_data)))

			#ACC_Y
			ACC_mean = np.mean(ACC_Y_data)/3
			ACC_std = np.std(ACC_Y_data, ddof=1)/3
			ACC_peak = (max(ACC_Y_data) - min(ACC_Y_data))/5
			ACC_peak_rms = sqrt(mean(square(ACC_Y_data)))/3
			ACC_peak_percent = 0
			for entry in ACC_Y_data:
				if entry >= abs(ACC_mean*1.25):
					ACC_peak_percent += 1

			my_ACC_coe.append(str(ACC_mean))
			my_ACC_coe.append(str(ACC_std))
			my_ACC_coe.append(str(ACC_peak))
			my_ACC_coe.append(str(ACC_peak_rms))
			my_ACC_coe.append(str(ACC_peak_percent/len(ACC_Y_data)))

			#ACC_Z
			ACC_mean = np.mean(ACC_Z_data)/3
			ACC_std = np.std(ACC_Z_data, ddof=1)/3
			ACC_peak = (max(ACC_Z_data) - min(ACC_Z_data))/5
			ACC_peak_rms = sqrt(mean(square(ACC_Z_data)))/3
			ACC_peak_percent = 0
			for entry in ACC_Z_data:
				if entry >= abs(ACC_mean*1.25):
					ACC_peak_percent += 1

			my_ACC_coe.append(str(ACC_mean))
			my_ACC_coe.append(str(ACC_std))
			my_ACC_coe.append(str(ACC_peak))
			my_ACC_coe.append(str(ACC_peak_rms))
			my_ACC_coe.append(str(ACC_peak_percent/len(ACC_Z_data)))

			#GYRO_X 
			GYRO_mean = np.mean(GYRO_X_data)/100
			GYRO_std = np.std(GYRO_X_data, ddof=1)/100
			GYRO_peak = (max(GYRO_X_data) - min(GYRO_X_data) )/200
			GYRO_peak_rms = sqrt(mean(square(GYRO_X_data)))/150
			GYRO_peak_percent= 0
			for entry in GYRO_X_data:
				if entry >= abs(GYRO_mean*1.25):
					GYRO_peak_percent += 1

			my_GYRO_coe.append(str(GYRO_mean))
			my_GYRO_coe.append(str(GYRO_std))
			my_GYRO_coe.append(str(GYRO_peak))
			my_GYRO_coe.append(str(GYRO_peak_rms))
			my_GYRO_coe.append(str(GYRO_peak_percent/len(GYRO_X_data)))

			#GYRO_Y
			GYRO_mean = np.mean(GYRO_Y_data)/100
			GYRO_std = np.std(GYRO_Y_data, ddof=1)/100
			GYRO_peak = (max(GYRO_Y_data) - min(GYRO_Y_data) )/200
			GYRO_peak_rms = sqrt(mean(square(GYRO_Y_data)))/150
			GYRO_peak_percent =0
			for entry in GYRO_Y_data:
				if entry >= abs(GYRO_mean*1.25):
					GYRO_peak_percent += 1
			my_GYRO_coe.append(str(GYRO_mean))
			my_GYRO_coe.append(str(GYRO_std))
			my_GYRO_coe.append(str(GYRO_peak))
			my_GYRO_coe.append(str(GYRO_peak_rms))
			my_GYRO_coe.append(str(GYRO_peak_percent/len(GYRO_Y_data)))

			#GYRO_Z
			GYRO_mean = np.mean(GYRO_Z_data)/100
			GYRO_std = np.std(GYRO_Z_data, ddof=1)/100
			GYRO_peak = (max(GYRO_Z_data) - min(GYRO_Z_data)) /200
			GYRO_peak_rms = sqrt(mean(square(GYRO_Z_data)))/150
			GYRO_peak_percent = 0
			for entry in GYRO_Z_data:
				if entry >= abs(GYRO_mean*1.25):
					GYRO_peak_percent += 1
			my_GYRO_coe.append(str(GYRO_mean))
			my_GYRO_coe.append(str(GYRO_std))
			my_GYRO_coe.append(str(GYRO_peak))
			my_GYRO_coe.append(str(GYRO_peak_rms))
			my_GYRO_coe.append(str(GYRO_peak_percent/len(GYRO_Z_data)))

			# spectrum_GYRO = fft.fft(GYRO_data_rms)
			# spectrum_GYRO[0] = 0
			# for i in xrange(len(spectrum_GYRO)):
			# 	if abs(spectrum_GYRO[i]) <100:
			# 		spectrum_GYRO[i] = 0

			# freq = fft.fftfreq(len(spectrum_GYRO))
			# for largest in heapq.nlargest(3, abs(spectrum_GYRO)):
			# 	my_GYRO_coe.append(str(largest))

			# my_GYRO_coe.append(str(GYRO_mean))
			# my_GYRO_coe.append(str(GYRO_std))
			# my_GYRO_coe.append(str(GYRO_peak))


			# spectrum_ACC = fft.fft(ACC_data_rms)
			# spectrum_ACC[0] = 0
			# for i in xrange(len(spectrum_ACC)):
			# 	if abs(spectrum_ACC[i]) <1:
			# 		spectrum_ACC[i] = 0

			# freq = fft.fftfreq(len(spectrum_ACC))
			# if 'REST' in action:
			# 	print action
			# 	plt.plot(freq ,spectrum_ACC)
			# 	plt.ylim([0,2])
			# 	plt.show()
			# 	break 
			# for largest in heapq.nlargest(3, abs(spectrum_ACC)):
			# 	my_ACC_coe.append(str(largest))



			#my_ACC_coe.append(str(ACC_peak_percent))





			# print len(my_ACC_coe)+len(my_GYRO_coe)
			line  += (' ').join(my_ACC_coe)+ ' '+ (' ').join(my_GYRO_coe) +' '

			#********CHANGE 0 to 1 for getting test data************
			line += '\n'
			with open('coefficient_data_test_update.txt', 'w') as f:
				f.write(line)
			print("wrote one line!!\n")

	else:
		time.sleep(1)