import sys

sys.path.insert(0, "/Users/jas/PycharmProjects/newGonzProj")

import matplotlib
matplotlib.use('MacOSX')

import birdsongs as bs
from birdsongs.utils import *

import numpy as np

import subprocess
# adjust path to wherever WriteAudio() put them
subprocess.call(["afplay", "audio/XC388622.wav"])

# After you have your audio in birdsong.signal (float32 in –1..1) and sampling rate in birdsong.sr:                                # block until done

paths = bs.Paths(
    root_path   = "/Users/jas/PycharmProjects/newGonzProj/birdsongs",
    audios_path = "/Users/jas/PycharmProjects/newGonzProj/birdsongs/examples/audios"
)

ploter = bs.Ploter(save=True)

print("Audios path:", paths.audios)
paths.ShowFiles()

root_path = "/Users/jas/PycharmProjects/newGonzProj/birdsongs"
audios_path = '/Users/jas/PycharmProjects/newGonzProj/birdsongs/examples/audios'

birdsong = bs.BirdSong(
    paths,
    file_id="XC388622",        # ID of one of the bird songs, only 3 available in the respository
    umbral_FF=1.0,
    NN=512,
    flim=(1e3, 20e3),
    split_method="freq",
    Nt=5000,
    umbral=0.05
)

ploter.Plot(birdsong, FF_on=False, SelectTime_on=True)
AudioPlay(birdsong)

# time_intervals = Positions(ploter.klicker)
time_intervals = np.array([[0.35362068, 0.49966724],
                           [0.65662832, 0.97055046],
                           [1.12231415, 1.3515189 ],
                           [1.43883499, 1.61502639],
                           [1.72105308, 1.87125755]])

print("You have selected {} syllables.".format(time_intervals.shape[0]))
[print(r"  - Syllable {}: t0 = {:.4f} s , tend = {:.4f} s".format(i, time_intervals[i,0], time_intervals[i,1])) for i in range(time_intervals.shape[0])];

syllable = bs.Syllable(birdsong, tlim=time_intervals[4], ide="syllable",
                       umbral_FF=0.5, Nt=30,  flim=(1e3,20e3), NN=birdsong.NN)
ploter.Plot(syllable, FF_on=True)
AudioPlay(syllable)

syllable_synth = syllable.Solve(syllable.p)

ploter.Syllables(syllable, syllable_synth)
ploter.PlotVs(syllable_synth)
ploter.PlotAlphaBeta(syllable_synth)
ploter.Result(syllable, syllable_synth)

AudioPlay(syllable_synth)

method_kwargs = {'method':'brute', 'Ns':5} #, "workers":-1
optimizer = bs.Optimizer(birdsong, method_kwargs=method_kwargs)

birdsong, synth_birdsong = optimizer.SongByTimes(time_intervals, NN=256)
Display(synth_birdsong.p)

Display(birdsong.p)

ploter.Plot(synth_birdsong)
# ploter.PlotAlphaBeta(synth_birdsong)

AudioPlay(synth_birdsong)

ploter.Plot(birdsong)
AudioPlay(birdsong)

birdsong.no_syllable = 1
ploter.Syllables(birdsong, synth_birdsong);

synth_bird = synth_birdsong.SolveAB(synth_birdsong.alpha, synth_birdsong.beta, 3700)
# # synth = SolveAB(syll, synth_birdsong.alphas, synth_birdsong.betas, 3700)

optimizer.optimal_gamma

synth_birdsong.id = "synth-birdsong"
synth_bird.paths = paths
ploter.Result(birdsong, synth_bird)
# ploter.PlotVs(synth_bird)
AudioPlay(synth_bird)

birdsong.WriteAudio()
synth_birdsong.WriteAudio()

