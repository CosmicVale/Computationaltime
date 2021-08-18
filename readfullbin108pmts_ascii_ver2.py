import numpy as np
import itertools
import sys
from sys import argv
import os
import time
from timeit import default_timer as timer
from datetime import timedelta


def int_or_float(s):
    ' Convert string from to int or float '
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return s
    
#position of centres
PMTloc =np.array([[-270.00, -156.00], [-270.00, -104.00], [-270.00, -52.00], [-270.00,  0.00], [-270.00,    52.00], [-270.00,   104.00], [-270.00,  156.00], [-225.00,  -182.00], [-225.00, -130.00], [-225.00, -78.00], [-225.00,  -26.00], [-225.00,  26.00], [-225.00,   78.00], [-225.00,   130.00], [-225.00,  182.00], [-180.00,  -208.00], [-180.00, -156.00], [-180.00, -104.00], [-180.00, -52.00], [-180.00,  0.00], [-180.00,    52.00], [-180.00,   104.00], [-180.00,  156.00], [-180.00,  208.00], [-135.00,  -234.00], [-135.00, -182.00], [-135.00, -130.00], [-135.00, -78.00], [-135.00,  -26.00], [-135.00,  26.00], [-135.00,   78.00], [-135.00,   130.00], [-135.00,  182.00], [-135.00,  234.00], [-90.00,   -208.00], [-90.00,  -156.00], [-90.00,  -104.00], [-90.00,  -52.00], [-90.00,   0.00], [-90.00, 52.00], [-90.00,    104.00], [-90.00,   156.00], [-90.00,   208.00], [-45.00,   -234.00], [-45.00,  -182.00], [-45.00,  -130.00], [-45.00,  -78.00], [-45.00,   -26.00], [-45.00,   26.00], [-45.00,    78.00], [-45.00,    130.00], [-45.00,   182.00], [-45.00,   234.00], [0.00, -208.00], [0.00,    -156.00], [0.00,    -104.00], [0.00,    -52.00], [0.00, 0.00], [0.00,   52.00], [0.00,  104.00], [0.00, 156.00], [0.00, 208.00], [45.00,    -234.00], [45.00,   -182.00], [45.00,   -130.00], [45.00,   -78.00], [45.00,    -26.00], [45.00,    26.00], [45.00, 78.00], [45.00, 130.00], [45.00,    182.00], [45.00,    234.00], [90.00,    -208.00], [90.00,   -156.00], [90.00,   -104.00], [90.00,   -52.00], [90.00,    0.00], [90.00,  52.00], [90.00, 104.00], [90.00,    156.00], [90.00,    208.00], [135.00,   -234.00], [135.00,  -182.00], [135.00,  -130.00], [135.00,  -78.00], [135.00,   -26.00], [135.00,   26.00], [135.00,    78.00], [135.00,    130.00], [135.00,   182.00], [135.00,   234.00], [180.00,   -208.00], [180.00,  -156.00], [180.00,  -104.00], [180.00,  -52.00], [180.00,   0.00], [180.00, 52.00], [180.00,    104.00], [180.00,   156.00], [180.00,   208.00], [225.00,   -182.00], [225.00,  -130.00], [225.00,  -78.00], [225.00,   -26.00], [225.00,   26.00], [225.00,    78.00], [225.00,    130.00], [225.00,   182.00]])

start = timer()

#checking number of arguments passed
n = len(sys.argv)
if n<3:
    print("Error number of arguments passed is incorrect. Try again...")

print("argv[0]: {0}".format(argv[0]))
print("argv[1]: {0}".format(argv[1]))
input_file = argv[1] 
output_file = argv[2] 
hits = []
with open(input_file, 'r') as DataIn:
    #for line in DataIn:
    #    hits += [line.split()]    # this line duplicates the hits array then appends (could use hits.append(line.split()))
    # But even better
    # Use list comprehension which avoids duplicating the data many times
    # Also convert to int or float on this pass
    hits = [[int_or_float(s) for s in line.split()] for line in DataIn]
    
totalPMT = 108

# Use one for loop
runid, eventid, time_fl, posx, posy, posz, partid = zip(*[(x[0], x[1], x[7], x[10], x[11], x[12], x[13]) for x in hits])


PMTs = [0]*108 #initial output signal
nscinti = 0 
nphoton = 0 
startscinti = 0 
zscinti = 0 
Etres = 100 #energy treshold
numb_22 = 0
numb_0 = 0
eventidnow = [0]*len(eventid) 
#eventidnow = [int(i) for i in eventIDnow]   # Seems unnecessary since already integer 0's from previous line
runidnow = [0]*len(runid)
#runidnow = [int(i) for i in runIDnow]       # Seems unnecessary since already integer 0's from previous line

with open(output_file, 'a+') as DataOut:  # Only open/close file once
    for i in range(len(eventid)):

        if ((eventid[i] > eventidnow[i]) or (runid[i] > runidnow[i])):

            if ((nscinti>0) and (partid[i]==22) and (nphoton>Etres)):  #check if last recorded event should be written 
                # Opening/closing in loop is very slow as noted by
                # https://stackoverflow.com/questions/23679495/python-when-writing-to-a-large-file-keep-the-file-open-or-to-open-it-and-appen
                # with open(output_file, 'a+') as DataOut:
                DataOut.write("{0} {1} {2}\n".format(startscinti, zscinti, ' '.join(map(str, PMTs))))


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
            if ((k<=totalPMT) and ((posx[i]-PMTloc[k][0])*(posx[i]-PMTloc[k][0]) + (posy[i]-PMTloc[k][1])*(posy[i]-PMTloc[k][1])<=23*23)):

                PMTs[k] += 1        
                nphoton += 1
                break


print("***PMTs ouptut signal for last scintillation event***")
for i in range(len(PMTs)):
    print("PMTs[{0}]: {1} ".format(i, PMTs[i]))


print("Number of total scintillation event: {0} Number scintillation photons: {1}".format(nscinti, nphoton))

end = timer()
print("Time elapsed writing: ", timedelta(seconds=end-start))
