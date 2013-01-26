from matplotlib import pyplot as plt
import sys
import marsyas
import marsyas_util

# Create top-level patch
net = marsyas_util.create(
    
        ["Series/extract_network",["SoundFileSource/src"
        ,"Windowing/win","Spectrum/spec","PowerSpectrum/pspec","Centroid/centr"
    ]])

filename = sys.argv[1]
fname = net.getControl("SoundFileSource/src/mrs_string/filename")
fname.setValue_string(filename)
net.linkControl("mrs_bool/hasData",
    "SoundFileSource/src/mrs_bool/hasData")
net.linkControl("mrs_string/filename",
    "SoundFileSource/src/mrs_string/filename")

x= net.getControl("mrs_realvec/processedData")
centroid =[]
while net.getControl("SoundFileSource/src/mrs_bool/hasData").to_bool():
    net.tick() # update time
    y = x.to_realvec()
    centroid.append(y[0])
plt.plot(centroid)
plt.show()
