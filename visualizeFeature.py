from matplotlib import pyplot as plt
import sys
import marsyas
import marsyas_util
import string
# Create top-level patch
net = marsyas_util.create(
    
        ["Series/extract_network",["SoundFileSource/src", ['Fanout/fea', ['ZeroCrossings/zcrs',
        ['Series/ctr',["Windowing/win","Spectrum/spec","PowerSpectrum/pspec","Centroid/centr"
    ]]]],"Annotator/annotator",
         "WekaSink/wsink"]])
filename = sys.argv[1]
fname = net.getControl("SoundFileSource/src/mrs_string/filename")
fname.setValue_string(filename)
net.linkControl("mrs_bool/hasData",
    "SoundFileSource/src/mrs_bool/hasData")
net.linkControl("mrs_string/filename",
    "SoundFileSource/src/mrs_string/filename")
#net.linkControl("Annotator/annotator/mrs_real/label",
#    "SoundFileSource/src/mrs_real/currentLabel")
net.linkControl("SoundFileSource/src/mrs_natural/nLabels",
    "WekaSink/wsink/mrs_natural/nLabels")
net.linkControl("WekaSink/wsink/mrs_string/currentlyPlaying",
    "SoundFileSource/src/mrs_string/currentlyPlaying")
net.updControl("WekaSink/wsink/mrs_string/filename",
    marsyas.MarControlPtr.from_string('Q5.arff'))

net.updControl("Annotator/annotator/mrs_bool/labelInFront", marsyas.MarControlPtr.from_bool(True))

net.updControl("WekaSink/wsink/mrs_string/labelNames", "Classical, Disco")
net.updControl("WekaSink/wsink/mrs_natural/nLabels", 2)

#lbl = filename

x= net.getControl("mrs_realvec/processedData")
zcr = []
centroid =[]
labels=[]

while net.getControl("SoundFileSource/src/mrs_bool/hasData").to_bool():
    net.tick() # update time
    y = x.to_realvec()
    currentlyPlaying = net.getControl("SoundFileSource/src/mrs_string/currentlyPlaying").to_string()
    label = -1.0*(string.find(currentlyPlaying,'classical'))
    labels.append(label)
    net.updControl("Annotator/annotator/mrs_real/label",label)
    centroid.append(y[0])
    zcr.append(y[1])
plt.plot(labels)
plt.show()
