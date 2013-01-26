from matplotlib import pyplot as plt
import sys
import marsyas
import marsyas_util
import string
# Create top-level patch
net = marsyas_util.create(
    
        ["Series/extract_network",["SoundFileSource/src", ['Fanout/fea', ['ZeroCrossings/zcrs',
        ['Series/ctr',["Windowing/win","Spectrum/spec","PowerSpectrum/pspec","Centroid/centr"
    ]]]]]])
dd=0.0
cc=0.0
dc=0.0
cd = 0.0
print range(1,len(sys.argv))
for fn in range(1,len(sys.argv)):
    filename = sys.argv[fn]
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
        centroid.append(y[1])
        zcr.append(y[0])
    #plt.plot(centroid)
    #plt.show()
#print centroid
    print len(centroid)
    for i in range(0,len(centroid)):
        if centroid[i] > 0.05 and zcr[i] > 0.14:
            if string.find(filename, 'disco') != -1:
                #print 'right'
                dd +=1.0
            else:
                #print 'not right'
                dc +=1.0
        else:
            if string.find(filename, 'class') != -1:
                cc +=1.0
                #print 'right'
            else:
                #print 'not right'
                cd +=1.0
classification_error = (cd + dc)/(cc + dd + dc + cd)
print classification_error
confusion_matrix = [[cc,dc],[cd,dd]]
print confusion_matrix
