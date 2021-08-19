import numpy as np
import itertools
import sys
from sys import argv
import os
import time
from timeit import default_timer as timer
from datetime import timedelta


start = timer()

#position of 108 PMTs centre
PMTloc =np.array([[-270.00,	-156.00], [-270.00,	-104.00], [-270.00,	-52.00], [-270.00,	0.00], [-270.00,	52.00], [-270.00,	104.00], [-270.00,	156.00], [-225.00,	-182.00], [-225.00,	-130.00], [-225.00,	-78.00], [-225.00,	-26.00], [-225.00,	26.00], [-225.00,	78.00], [-225.00,	130.00], [-225.00,	182.00], [-180.00,	-208.00], [-180.00,	-156.00], [-180.00,	-104.00], [-180.00,	-52.00], [-180.00,	0.00], [-180.00,	52.00], [-180.00,	104.00], [-180.00,	156.00], [-180.00,	208.00], [-135.00,	-234.00], [-135.00,	-182.00], [-135.00,	-130.00], [-135.00,	-78.00], [-135.00,	-26.00], [-135.00,	26.00], [-135.00,	78.00], [-135.00,	130.00], [-135.00,	182.00], [-135.00,	234.00], [-90.00,	-208.00], [-90.00,	-156.00], [-90.00,	-104.00], [-90.00,	-52.00], [-90.00,	0.00], [-90.00,	52.00], [-90.00,	104.00], [-90.00,	156.00], [-90.00,	208.00], [-45.00,	-234.00], [-45.00,	-182.00], [-45.00,	-130.00], [-45.00,	-78.00], [-45.00,	-26.00], [-45.00,	26.00], [-45.00,	78.00], [-45.00,	130.00], [-45.00,	182.00], [-45.00,	234.00], [0.00,	-208.00], [0.00,	-156.00], [0.00,	-104.00], [0.00,	-52.00], [0.00,	0.00], [0.00,	52.00], [0.00,	104.00], [0.00,	156.00], [0.00,	208.00], [45.00,	-234.00], [45.00,	-182.00], [45.00,	-130.00], [45.00,	-78.00], [45.00,	-26.00], [45.00,	26.00], [45.00,	78.00], [45.00,	130.00], [45.00,	182.00], [45.00,	234.00], [90.00,	-208.00], [90.00,	-156.00], [90.00,	-104.00], [90.00,	-52.00], [90.00,	0.00], [90.00,	52.00], [90.00,	104.00], [90.00,	156.00], [90.00,	208.00], [135.00,	-234.00], [135.00,	-182.00], [135.00,	-130.00], [135.00,	-78.00], [135.00,	-26.00], [135.00,	26.00], [135.00,	78.00], [135.00,	130.00], [135.00,	182.00], [135.00,	234.00], [180.00,	-208.00], [180.00,	-156.00], [180.00,	-104.00], [180.00,	-52.00], [180.00,	0.00], [180.00,	52.00], [180.00,	104.00], [180.00,	156.00], [180.00,	208.00], [225.00,	-182.00], [225.00,	-130.00], [225.00,	-78.00], [225.00,	-26.00], [225.00,	26.00], [225.00,	78.00], [225.00,	130.00], [225.00,	182.00]])
#print(PMTloc.shape)

dir_path = os.path.dirname(os.path.realpath(__file__))
print("\nDirectory path: ", dir_path)

#chechking number of arguments passed
n = len(sys.argv)
if n<3:
    print("Error number of arguments passed is incorrect. Try again...")

print("argv[0]: {0}".format(argv[0]))
print("argv[1]: {0}".format(argv[1]))
input_file = argv[1] #name of the file to read given as first command line argument
output_file = argv[2] #name of the file to write output given as second argument
hits = []
with open(input_file, 'r') as DataIn:
    for line in DataIn:
        hits += [line.split()]


#print(hits[1])
totalPMT = 108
runID = [x[0] for x in hits] #define list with runID values, its the column with index 0 of hits
runid=[int(i) for i in runID] #convert runID list into a list of float

eventID = [x[1] for x in hits]
eventid=[int(i) for i in eventID]
#print(len(eventid))

time = [x[7] for x in hits]
time_fl = [float(i) for i in time]

posX = [x[10] for x in hits]
posx = [float(i) for i in posX]

posY = [x[11] for x in hits]
posy = [float(i) for i in posY]

posZ = [x[12] for x in hits]
posz = [float(i) for i in posZ]

partID = [x[13] for x in hits]
partid = [int(i) for i in partID]

PMTs = [0]*108 #initial PMT output signal
#print(len(PMTs))
nscinti = 0 #number of scintillation
nphoton = 0 #number of scintillation photon
startscinti = 0 #start time of scintillation
zscinti = 0 #DoI or posZ of gamma interaction that leads to scinti
Etres = 100 #energy treshold
numb_22 = 0
numb_0 = 0
eventIDnow = [0]*len(eventid) #list full of 0, used to check if eventID changes 
eventidnow = [int(i) for i in eventIDnow]
#print(len(eventidnow))
runIDnow = [0]*len(runid) #list full of 0, used to check if runID changes
runidnow = [int(i) for i in runIDnow]

end = timer()
print("Time elapsed reading: ", timedelta(seconds=end-start))

start_loop = timer()
    
for i in range(len(eventid)):
    if ((eventid[i] > eventidnow[i]) or (runid[i] > runidnow[i])):
        
        if ((nscinti>0) and (partid[i]==22) and (nphoton>Etres)):  #check if last recorded event should be written 
            
            print("Writing output data to file")
            with open(output_file, 'a+') as DataOut:
                DataOut.write("{0} {1} {2}\n".format(startscinti, zscinti, ' '.join(map(str, PMTs))))
                
            
       # print("***EVENT OR RUN ID HAS CHANGED***")
        for l in range(len(eventidnow)): #updating values of eventidnow and runidnow
            eventidnow[l] =  eventid[i]
            runidnow[l] = runid[i]
           
        startscinti = time_fl[i]
        zscinti = posz[i]
        nphoton = 0
        nscinti += 1
        for j in range(len(PMTs)):
            PMTs[j] = 0

   
    for k in range(len(PMTs)):
        if ((posx[i]-PMTloc[k][0])*(posx[i]-PMTloc[k][0]) + (posy[i]-PMTloc[k][1])*(posy[i]-PMTloc[k][1])<=23*23):
           
            PMTs[k] += 1
            nphoton += 1
            break
       
   
print("***PMTs ouptut signal for last scintillation event***")
for i in range(len(PMTs)):
    print("PMTs[{0}]: {1} ".format(i, PMTs[i]))


print("Number of total scintillation event: {0} Number scintillation photons: {1}".format(nscinti, nphoton))

end_loop = timer()
print("Time elapsed writing: ", timedelta(seconds=end_loop-start_loop))

            
