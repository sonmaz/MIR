#Creating a sine wave with the same frequency as the input file.

from matplotlib import pyplot as plt
import sys
import marsyas
import marsyas_util

# Create top-level patch
centList = ["Series/extract_network",["SoundFileSource/src","Windowing/win","Spectrum/spec","PowerSpectrum/pspec","Centroid/centr"]]
sineList =  ["Series/sinnet",["SineSource/src1", "Gain/gain"]]

net1 = marsyas_util.create(centList)
net2 = marsyas_util.create(
["Series/sound",
          [["Fanout/snd",
              [sineList, "SoundFileSource/src2"]],
              ['Fanout/sinks',['SoundFileSink/sfs',"AudioSink/as"]]
              ]
      ]
)

filename = sys.argv[1]
fname1 = net1.getControl("SoundFileSource/src/mrs_string/filename")
fname1.setValue_string(filename)

fname2 = net2.getControl("Fanout/snd/SoundFileSource/src2/mrs_string/filename")
fname2.setValue_string(filename)

net1.linkControl("mrs_bool/hasData", "SoundFileSource/src/mrs_bool/hasData")

x= net1.getControl("mrs_realvec/processedData")

centroid = 0

net2.updControl("Fanout/sinks/AudioSink/as/mrs_bool/initAudio", marsyas.MarControlPtr.from_bool(True));
fout = filename.replace(".au", "")
net2.updControl("Fanout/sinks/SoundFileSink/sfs/mrs_string/filename", fout+'centr-src.au');



while net1.getControl("mrs_bool/hasData").to_bool():
    centroid = centroid*22050
    freq = net2.getControl("Fanout/snd/Series/sinnet/SineSource/src1/mrs_real/frequency");
    freq.setValue_real(centroid)
    net2.tick()
    net1.tick()
    y = x.to_realvec()
    centroid = y[0]

