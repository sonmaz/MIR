from matplotlib import pyplot as plt
import sys
import marsyas
import marsyas_util

# Create top-level patch
net = marsyas_util.create(
    
        ["Series/extract_network",["SoundFileSource/src", ['Fanout/fea', ['ZeroCrossings/zcrs',
        ['Series/ctr',["Windowing/win","Spectrum/spec","PowerSpectrum/pspec","Centroid/centr"
    ]]]]]])


filename = sys.argv[1]
fname = net.getControl("SoundFileSource/src/mrs_string/filename")
fname.setValue_string(filename)
net.linkControl("mrs_bool/hasData",
    "SoundFileSource/src/mrs_bool/hasData")
net.linkControl("mrs_string/filename",
    "SoundFileSource/src/mrs_string/filename")

x= net.getControl("mrs_realvec/processedData")
zcr = []
centroid =[]
while net.getControl("SoundFileSource/src/mrs_bool/hasData").to_bool():
    net.tick() # update time
    y = x.to_realvec()
    centroid.append(y[0])
    zcr.append(y[1])
#plt.plot(zcr)
#plt.show()

labels = []
#print centroid
print (len(centroid)-1)
for i in range(0,len(centroid)-1):
    if centroid[i] > 0.4*max(centroid) and zcr[i] > 0.4*max(zcr):
        labels.append(1)
    else:
        labels.append(0)

plt.plot(labels)
plt.plot(zcr)
plt.show()
