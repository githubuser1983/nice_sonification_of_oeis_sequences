import numpy as np
from getkey import getkey, keys
import random, sys, pickle
from scamp import Session, Ensemble, current_clock
from compute_knn_model import *
from music21.pitch import Pitch

from scamp import Session, Ensemble
from scamp._soundfont_host import get_best_preset_match_for_name

def get_general_midi_number_for_instrument_name(p,sf):
    ensemble = Ensemble(default_soundfont=sf)
    return (get_best_preset_match_for_name(p,which_soundfont=ensemble.default_soundfont)[0]).preset


generalSF = "/usr/share/sounds/sf3/MuseScore_General.sf3"
pianoSF = "~/Dokumente/MuseScore3/SoundFonts/4U-Mellow-Steinway-v3.6.sf2"

if len(sys.argv) == 2:
    conf = readConfiguration(sys.argv[1])
else:
    conf = {
        "soundfont": pianoSF, 
        "loopKnn" : False,
        "knn_nr_neighbors" : 5,
        "knn_is_reverse" : True,
        "instrumentName" : "Mellow Steinway",
        "midiFileName" : "./midi/live_music_grand_piano.mid",
        "knn_model" : "./knn_models/knn.pkl"
    }
    writeConfiguration("./scamp-piano-configurations/start-conf.yaml",conf)

loopKnn = conf["loopKnn"]    
#knn_nr_neighbors = conf["knn_nr_neighbors"]
knn_is_reverse=conf["knn_is_reverse"]    
instrumentName = conf["instrumentName"]    
midiFileName = conf["midiFileName"]
instrumentMidiNumber = get_general_midi_number_for_instrument_name(instrumentName,generalSF)    
std = [instrumentName]
sf = conf["soundfont"]
knn_model = load_knn(conf["knn_model"])
max_nr_knn = (conf["max_nr_knn"])
min_nr_knn = (conf["min_nr_knn"])
seq = [int(x) for x in conf["sequence"].split(",")]
startNote = [(conf[c]) for c in ["start_pitch","start_duration","start_volume","start_is_rest"]]
startNote = int(startNote[0]),float(startNote[1]),int(startNote[2]),int(startNote[3])
tempo = conf["tempo"]
seq_mod = conf["sequence_modulo"]

print(seq)

def kk(a,b):
    return (2*a*b)/(a**2+b**2)

def dist(kk,a,b):
    return sqrt(kk(a,a)+kk(b,b)-2*kk(a,b))

def main():
    print("    \n    ".join(["- "+str(x) for x in seq]))
    dists = [dist(kk,seq[i],seq[i+1]) for i in range(len(seq)-1)]
    pitch,duration,volume,isPause = startNote #60,0.5,64,0
    #startNote = pitch,duration,volume,isPause
    inds = [[startNote]]
    for number in seq:
        new_row = np.array([pitch,duration,volume,isPause])
        two_octaves = pitch//24
        nbrs,notes = knn_model[two_octaves]
        bm = findBestMatches(nbrs,new_row,n_neighbors=max(min_nr_knn,min(max_nr_knn,abs(number % seq_mod))),reverse=knn_is_reverse)
        #print([notes[b] for b in bm])
        for b in bm:
            pitch,duration,volume,isPause = notes[b]
            note = pitch,duration,volume,isPause
            inds[0].append(note)
    fn = midiFileName
    writePitches(fn,inds,tempo=tempo,instrument=[instrumentMidiNumber],add21=False,start_at= [0,0],durationsInQuarterNotes=True)

if __name__=="__main__":
    main()