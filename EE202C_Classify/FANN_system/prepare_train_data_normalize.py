# Scientific libraries
# import plotly.plotly as py
# import plotly.graph_objs as go
import numpy as np
from numpy import genfromtxt
from numpy import mean, sqrt, square, arange
import os
import os.path
import random
import sys
import numpy.fft as fft
import heapq

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
action = ''

trainfile = open('coefficient_data_train.txt','w')
testfile = open('coefficient_data_test.txt','w')

for dirpath, dirnames, filenames in os.walk("."):
    for filename in [f for f in filenames if f.endswith(".csv")]:
    	if 'cook' in os.path.join(dirpath, filename):
    		action = 'COOK'
    	elif 'read' in os.path.join(dirpath, filename):
    		action = 'READ'
    	elif 'rest' in os.path.join(dirpath, filename):
    		action = 'REST'
    	elif 'type' in os.path.join(dirpath, filename):
    		action = 'TYPE'
    	elif 'walk' in os.path.join(dirpath, filename):
    		action = 'WALK'	
        if 'RIGHT_WRIST' in filename:
        	train_data_RIGHT_Wrist.append((genfromtxt(os.path.join(dirpath, filename), delimiter=','),action))
        elif 'LEFT_WRIST' in filename:
        	train_data_LEFT_Wrist.append((genfromtxt(os.path.join(dirpath, filename), delimiter=','),action))
        elif 'ELBOW' in filename:
        	train_data_ELBOW.append((genfromtxt(os.path.join(dirpath, filename), delimiter=','),action))
        print filename

for (data, action) , (data_2, action_2) ,(data_3, action_3)in zip(train_data_RIGHT_Wrist, train_data_LEFT_Wrist, train_data_ELBOW):

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





	print len(my_ACC_coe)+len(my_GYRO_coe)
	line  += (' ').join(my_ACC_coe)+ ' '+ (' ').join(my_GYRO_coe) +' '

	#********CHANGE 0 to 1 for getting test data************
	if 1: 
		# print action
		line += '\n'
		testfile.write(line)
	else:
		if 'COOK' in action:
			line += '1 0 0 0 0 0\n'
		elif 'READ' in action:
			line += '0 1 0 0 0 0\n'
		elif 'REST' in action:
			line += '0 0 1 0 0 0\n'
		elif 'TYPE' in action:
			line += '0 0 0 1 0 0\n'
		elif 'WALK' in action:
			line += '0 0 0 0 1 0\n'
		elif 'GROOM' in action:
			line += '0 0 0 0 0 1\n'
		trainfile.write(line)

trainfile.close()
testfile.close()
lines = open('coefficient_data_train.txt').readlines()
random.shuffle(lines)

#***********Change this***********    ------> (# of entries, #of features, # of states)
open('coefficient_data_train.txt', 'w').writelines(["2 54 4\n"]+lines)



